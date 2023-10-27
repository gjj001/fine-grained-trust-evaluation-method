import random
import math


class Node:
    '''
    定义一个节点类
    '''
    id = -1
    R = 0  # 节点行为可靠性
    abnormal_factor = 0  # 异常因子
    delay_factor = 0  # 时延因子

    def __init__(self, behavior, value):
        '''
        初始化节点属性
        :param behavior: 节点行为序号，1为行为B1，2为行为B2，3为行为B3
        :param value: 节点信任值
        '''
        self.behavior = behavior
        self.value = value

    def behav1(self):
        '''
        行为B1：良好参与方：行为良好、稳定性高（异常度低，时延低/异常因子和时延因子都高）
              异常因子abnormal_factor 在0.9-1之间
              时延因子delay_factor 在0.9-1之间
        :return:
        '''
        self.abnormal_factor = random.randint(11000, 13000) / 10000  # 异常因子
        self.delay_factor = random.randint(11000, 13000) / 10000  # 时延因子
        if self.abnormal_factor >= 1.275 and self.delay_factor >= 1.275:
            self.R = 1
        else:
            self.R = (1 / (1 + math.exp(-self.abnormal_factor))) * self.delay_factor  # 可靠性计算

    def behav2(self):
        '''
        行为B2：恶意参与方：可靠性差、稳定性高（异常度高、时延高/异常因子低，时延因子低）
              异常因子abnormal_factor 在0-0.2之间
              时延因子delay_factor 在0-0.2之间
        :return:
        '''
        self.abnormal_factor = random.randint(0, 7000) / 10000  # 异常因子
        self.delay_factor = random.randint(0, 7000) / 10000  # 时延因子
        self.R = (1 / (1 + math.exp(-self.abnormal_factor))) * self.delay_factor  # 可靠性计算

    def __str__(self):
        return 'abnormal_factor:' + str(self.abnormal_factor) + '; delay_factor:' + str(self.delay_factor) + '; R:' + str(self.R) + ';'


# 计算当前信任值
def current_trust(HL, interation_count):  # 当前行为可靠性 历史交互次数（阈值70）
    Rcurr = HL[19][0]
    if Rcurr > 0.5:
        if interation_count <= 70 and interation_count >= 0:
            g = 0.0001 * interation_count * interation_count + 0.5
        else:
            g = 1
        return 0.5 + g * (Rcurr - 0.5)
    else:
        return 0


# 计算历史信任值
def historical_trust(HL):  # 历史交互信息表（部分）
    hist = 0
    for i in range(19):
        hist += HL[i][0] * (math.pow(2, -(19 - i)))
    return hist


# 计算直接信任值
def direct_trust(current_trust_value, historical_trust_value, interation_count, current_stability, HL, Thist):  # 当前信任值 历史信任值 历史交互次数 当前行为稳定性 历史交互信息表（部分） 历史信任值
    if interation_count > 1:
        shuxi = 1 - (1 / (pow((math.exp(interation_count - 1)), 0.1) + 1))
    else:
        shuxi = 0
    whist = shuxi * current_stability
    wcurr = 1 - whist
    total = 0
    Rcurr = HL[19][0]
    if Rcurr > 0.5:
        for i in range(19):
            if HL[18 - i][0] > 0.5:
                total += 1
            else:
                break
        n = 0.001 * pow(2, total)
        if n > 1:
            n = 1
        return ((whist * historical_trust_value + wcurr * current_trust_value) - Thist) * n + Thist
    elif Rcurr <= 0.5:
        return whist * historical_trust_value + wcurr * current_trust_value


# 计算推荐信任度
def recommended_trust(RL):  # 推荐信息表（部分）
    HR = 0
    sum = 0
    for i in range(20):
        HR += RL[i][0]
    if HR == 0:  # 如果没有推荐服务器
        return 0
    else:
        for i in range(20):
            sum += (RL[i][0] / HR) * RL[i][1]
    return sum


# 计算综合信任度
def comprehensive_trust (recommended_trust_value, direct_trust_value, interation_count, RL, id):  # 推荐信任度 直接信任度 历史交互次数列表 推荐信息列表 节点id
    if sum(interation_count) == 0:
        a = 0
    else:
        a = interation_count[id] / (sum(interation_count) / 100)
    addR = []
    for i in range(100):
        total_R = 0
        for j in range(20):
            total_R += RL[i][j][0]
        addR.append(total_R)
    if sum(addR) == 0:
        b = 0
    else:
        b = addR[id] / (sum(addR) / 100)
    if a == 0 and b == 0:
        weight = 0
    elif a == 0 and b != 0:
        weight = 0.5
    else:
        weight = b / (a + b)
    wd = 1 - weight
    return weight * recommended_trust_value + wd * direct_trust_value


# 计算综合信任度整体函数
def function(R, list_interation_count, listHL, listRL, listThist, S, id):  # 当前行为可靠性 历史交互次数（列表） 历史交互信息表（列表） 推荐信息表（列表） 行为稳定性 节点id
    Tcurr = current_trust(listHL[id], list_interation_count[id])  # 当前信任值
    Thist = historical_trust(listHL[id])  # 历史信任值
    Tdirect_trust = direct_trust(Tcurr, Thist, list_interation_count[id], S, listHL[id], listThist[id])  # 直接信任值
    Trecommended_trust = recommended_trust(listRL[id])  # 推荐信任度
    TTT = comprehensive_trust (Trecommended_trust, Tdirect_trust, list_interation_count, listRL, id)  # 综合信任度
    return TTT


B1 = B2 = B3 = B4 = B5 = B6 = B7 = B8 = 0
count1 = []
for i in range(100):  # 10 5 10 5
    if B1 == 10:
        B2 += 1
        count1.append(0)
        if B2 == 5:
            B1 = 0
    else:
        count1.append(1)
        B1 += 1
        B2 = 0
count2 = []
for i in range(100):  # 10 10 10 10
    if B3 == 10:
        B4 += 1
        count2.append(0)
        if B4 == 10:
            B3 = 0
    else:
        count2.append(1)
        B3 += 1
        B4 = 0
count3 = []
for i in range(100):  # 1 1 1 1
    if B5 == 1:
        B6 += 1
        count3.append(0)
        if B6 == 1:
            B5 = 0
    else:
        count3.append(1)
        B5 += 1
        B6 = 0
count4 = []
for i in range(100):  # 5 10 5 10
    if B7 == 5:
        B8 += 1
        count4.append(0)
        if B8 == 10:
            B7 = 0
    else:
        count4.append(1)
        B7 += 1
        B8 = 0

# HL存储1-100节点的历史交互信息表，每个节点最多存储20个历史交互信息
k1 = 0
list_HL = []
for i in range(100):
    list_HL.append([[0.5, 0.5]])
    for j in range(19):
        list_HL[k1].append([0.5, 0.5])
    k1 += 1

# RL存储1-100节点的推荐信息表，每个节点最多存储20个推荐信任值（交互次数随机给出1-100之间）
k2 = 0
list_RL = []
for i in range(100):
    list_RL.append([[0, 0]])
    for j in range(19):
        list_RL[k2].append([0, 0])
    k2 += 1

# 存储1-100个节点的历史交互次数，最初1-100节点的历史交互次数都为0
list_interation_count = []
for i in range(100):
    list_interation_count.append(0)

# 存储1-100个节点的历史信任度值，最初1-100节点的历史信任度值都定义为0.5
list_Thist = []
for i in range(100):
    list_Thist.append(0.5)

# 存储1-100个节点的推荐服务器数量，最初1-100节点的推荐服务器数量都为99
list_renum = []
for i in range(100):
    list_renum.append(99)


def main(f):
    # 100个周期
    print('{},{},{},{},{},{}'.format(0, 0, 0, 0, 0, 0.5), file=f)
    for circul in range(100):
        # print('第{}个周期'.format(circul + 1),file=f)
        # print('-' * 80,file=f)
        # 每个周期100个节点全部作为候选参与者参与联邦学习，但是每次服务器S1只从100个节点中选取可靠性最高的20个本地模型进行聚合
        # 100个节点中：1-20 行为B1; 20-40 行为B2; 40-60 行为B3(1); 60-80 行为B3(2); 80-100 行为B3(3)
        # 遍历100个节点，初始化节点类
        for i in range(1):
            add = 0  # 10次B1 5次B2

            # 行为B3
            # 稳定性差（交替提供良好行为与恶意行为，进行x次良好行为后，再进行y次恶意行为）
            # ① x > y 10次行为B1，5次行为B2
            # ② x = y 10次行为B1，10次行为B2
            # ③ x < y 5次行为B1，10次行为B2

            # p = Node(2, list_Thist[i])
            # p.behav2()
            # list_HL[i].append([p.R, 0])
            # del list_HL[i][0]  # 更新历史信息表
            # for j in range(19):
            #     add += abs(list_HL[i][j + 1][0] - list_HL[i][j][0])
            # S = add / 19
            # list_HL[i][19][1] = S
            # list_interation_count[i] += 1
            # for update_value in range(20):
            #     recommended_trust_result = 0
            #     recommended_trust_k1 = 1
            #     recommended_trust_HL = [[[0.5, 0.5]]]  # 推荐服务器 历史交互表
            #     for nn in range(19):
            #         recommended_trust_HL[0].append([0.5, 0.5])
            #     for ll in range(99):
            #         recommended_trust_HL.append([[0, 0]])
            #         for nn in range(19):
            #             recommended_trust_HL[recommended_trust_k1].append([0, 0])
            #         recommended_trust_k1 += 1
            #     recommended_trust_k2 = 0
            #     recommended_trust_RL = []  # 推荐服务器 推荐信息表
            #     for nn in range(100):
            #         recommended_trust_RL.append([[0, 0]])
            #         for ll in range(19):
            #             recommended_trust_RL[recommended_trust_k2].append([0, 0])
            #         recommended_trust_k2 += 1
            #     recommended_trust_interation_count = []  # 推荐服务器 历史交互次数
            #     for ll in range(100):
            #         recommended_trust_interation_count.append(0)
            #     recommended_trust_Thist = []  # 推荐服务器  历史信任值
            #     recommended_trust_Thist.append(0.5)
            #     list_RL[i][update_value][0] = random.randint(0, 100)  # 随机产生推荐服务器与节点的历史交互次数
            #     for caculate in range(list_RL[i][update_value][0]):  # 以实际交互为准
            #         recommended_trust_add = 0
            #         recommended_trust_p = Node(2, list_Thist[i])
            #         recommended_trust_p.behav2()
            #         recommended_trust_HL[0].append([recommended_trust_p.R, 0])
            #         del recommended_trust_HL[0][0]
            #         for j in range(19):
            #             recommended_trust_add += abs(recommended_trust_HL[0][j + 1][0] - recommended_trust_HL[0][j][0])
            #         recommended_trust_S = recommended_trust_add / 19
            #         recommended_trust_HL[0][19][1] = recommended_trust_S
            #         recommended_trust_interation_count[0] += 1  # 更新历史交互次数列表
            #         recommended_trust_direct_hist=direct_trust(current_trust(recommended_trust_HL[0], recommended_trust_interation_count[0]), historical_trust(recommended_trust_HL[0]), recommended_trust_interation_count[0], recommended_trust_HL[0][19][1], recommended_trust_HL[0],recommended_trust_Thist[0])
            #         recommended_trust_result = hanshhu(recommended_trust_p.R, recommended_trust_interation_count, recommended_trust_HL, recommended_trust_RL, recommended_trust_Thist,recommended_trust_S, 0)
            #         recommended_trust_Thist[0]=recommended_trust_direct_hist
            #     list_RL[i][update_value][1] = recommended_trust_result
            # direct_hist=direct_trust(current_trust(list_HL[i], list_interation_count[i]), historical_trust(list_HL[i]), list_interation_count[i], list_HL[i][19][1], list_HL[i],list_Thist[i])
            # result = function(p.R, list_interation_count, list_HL, list_RL, list_Thist, list_HL[i][19][1], i)
            # print('{},{},{},{},{},{}'.format(circul+1,current_trust(list_HL[i], list_interation_count[i]),historical_trust(list_HL[i]),direct_hist,recommended_trust(list_RL[i]),result),file=f)
            # # print(list_HL[i], file=f)
            # print(list_RL[i], file=f)
            # print('S {} ;    current_hist {} ;    Rcurr: {} ;'.format(list_HL[i][19][1],list_Thist[i],p.R), file=f)
            # print('dq: {}'.format(current_trust(list_HL[i], list_interation_count[i])),file=f)
            # print('ls: {}'.format(historical_trust(list_HL[i])),file=f)
            # print('zj: {}'.format(direct_hist),file=f)
            # print('tj: {}'.format(recommended_trust(list_RL[i])),file=f)
            # print('T：{} '.format(result),file=f)
            # list_Thist[i] = direct_hist

            p = Node(3, list_Thist[i])
            if count4[circul] == 1:
                p.behav1()
                list_HL[i].append([p.R, 0])
                del list_HL[i][0]  # 更新历史信息表
                for j in range(19):
                    add += abs(list_HL[i][j + 1][0] - list_HL[i][j][0])
                S = add / 19
                list_HL[i][19][1] = S
            elif count4[circul] == 0:
                p.behav2()
                list_HL[i].append([p.R, 0])
                del list_HL[i][0]  # 更新历史信息表
                for j in range(19):
                    add += abs(list_HL[i][j + 1][0] - list_HL[i][j][0])
                S = add / 19
                list_HL[i][19][1] = S
            list_interation_count[i] += 1

            # 更新推荐列表
            for update_value in range(20):
                recommended_trust_result = 0
                recommended_trust_k1 = 1
                recommended_trust_HL = [[[0.5, 0.5]]]  # 推荐服务器 历史交互表
                for nn in range(19):
                    recommended_trust_HL[0].append([0.5, 0.5])
                for ll in range(99):
                    recommended_trust_HL.append([[0, 0]])
                    for nn in range(19):
                        recommended_trust_HL[recommended_trust_k1].append([0, 0])
                    recommended_trust_k1 += 1
                recommended_trust_k2 = 0
                recommended_trust_RL = []  # 推荐服务器 推荐信息表
                for nn in range(100):
                    recommended_trust_RL.append([[0, 0]])
                    for ll in range(19):
                        recommended_trust_RL[recommended_trust_k2].append([0, 0])
                    recommended_trust_k2 += 1
                recommended_trust_interation_count = []  # 推荐服务器 历史交互次数
                for ll in range(100):
                    recommended_trust_interation_count.append(0)
                recommended_trust_Thist = []  # 推荐服务器  历史信任值
                recommended_trust_Thist.append(0.5)
                list_RL[i][update_value][0] = random.randint(0, 100)  # 随机产生推荐服务器与节点的历史交互次数
                for caculate in range(list_RL[i][update_value][0]):  # 以实际交互为准
                    recommended_trust_add = 0
                    if count4[caculate] == 1:
                        recommended_trust_p = Node(1, list_Thist[i])
                        recommended_trust_p.behav1()
                        recommended_trust_HL[0].append([recommended_trust_p.R, 0])
                        del recommended_trust_HL[0][0]
                        for j in range(19):
                            recommended_trust_add += abs(recommended_trust_HL[0][j + 1][0] - recommended_trust_HL[0][j][0])
                        recommended_trust_S = recommended_trust_add / 19
                        recommended_trust_HL[0][19][1] = recommended_trust_S
                        recommended_trust_interation_count[0] += 1  # 更新历史交互次数列表
                        recommended_trust_direct_hist = direct_trust(current_trust(recommended_trust_HL[0], recommended_trust_interation_count[0]), historical_trust(recommended_trust_HL[0]),
                                                recommended_trust_interation_count[0], recommended_trust_HL[0][19][1], recommended_trust_HL[0], recommended_trust_Thist[0])
                        recommended_trust_result = function(recommended_trust_p.R, recommended_trust_interation_count, recommended_trust_HL, recommended_trust_RL, recommended_trust_Thist,
                                                 recommended_trust_S, 0)
                        recommended_trust_Thist[0] = recommended_trust_direct_hist
                    elif count4[caculate] == 0:
                        recommended_trust_p = Node(2, list_Thist[i])
                        recommended_trust_p.behav2()
                        recommended_trust_HL[0].append([recommended_trust_p.R, 0])
                        del recommended_trust_HL[0][0]
                        for j in range(19):
                            recommended_trust_add += abs(recommended_trust_HL[0][j + 1][0] - recommended_trust_HL[0][j][0])
                        recommended_trust_S = recommended_trust_add / 19
                        recommended_trust_HL[0][19][1] = recommended_trust_S
                        recommended_trust_interation_count[0] += 1  # 更新历史交互次数列表
                        recommended_trust_direct_hist = direct_trust(current_trust(recommended_trust_HL[0], recommended_trust_interation_count[0]), historical_trust(recommended_trust_HL[0]),
                                                recommended_trust_interation_count[0], recommended_trust_HL[0][19][1], recommended_trust_HL[0], recommended_trust_Thist[0])
                        recommended_trust_result = function(recommended_trust_p.R, recommended_trust_interation_count, recommended_trust_HL, recommended_trust_RL, recommended_trust_Thist,
                                                 recommended_trust_S, 0)
                        recommended_trust_Thist[0] = recommended_trust_direct_hist
                list_RL[i][update_value][1] = recommended_trust_result
            direct_hist = direct_trust(current_trust(list_HL[i], list_interation_count[i]), historical_trust(list_HL[i]), list_interation_count[i], list_HL[i][19][1],
                            list_HL[i], list_Thist[i])
            result = function(p.R, list_interation_count, list_HL, list_RL, list_Thist, list_HL[i][19][1], i)
            print('{},{},{},{},{},{}'.format(circul + 1, current_trust(list_HL[i], list_interation_count[i]), historical_trust(list_HL[i]), direct_hist,
                                             recommended_trust(list_RL[i]), result), file=f)
            list_Thist[i] = direct_hist

        # print('\n',file=f)


if __name__ == '__main__':
    with open('C:\\Users\\12549\\Desktop\\fout.txt', 'w') as f:
        main(f)
