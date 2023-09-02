import random
import math


class Node:
    '''
    定义一个节点类
    '''
    id = -1
    R = 0  # 节点行为可靠性
    aaa = 0  # 异常因子
    bbb = 0  # 时延因子

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
              异常因子aaa 在0.9-1之间
              时延因子bbb 在0.9-1之间
        :return:
        '''
        self.aaa = random.randint(11000, 13000) / 10000  # 异常因子
        self.bbb = random.randint(11000, 13000) / 10000  # 时延因子
        if self.aaa >= 1.275 and self.bbb >= 1.275:
            self.R = 1
        else:
            self.R = (1 / (1 + math.exp(-self.aaa))) * self.bbb  # 可靠性计算

    def behav2(self):
        '''
        行为B2：恶意参与方：可靠性差、稳定性高（异常度高、时延高/异常因子低，时延因子低）
              异常因子aaa 在0-0.2之间
              时延因子bbb 在0-0.2之间
        :return:
        '''
        self.aaa = random.randint(0, 7000) / 10000  # 异常因子
        self.bbb = random.randint(0, 7000) / 10000  # 时延因子
        self.R = (1 / (1 + math.exp(-self.aaa))) * self.bbb  # 可靠性计算

    def __str__(self):
        return 'aaa:' + str(self.aaa) + '; bbb:' + str(self.bbb) + '; R:' + str(self.R) + ';'


# 计算当前信任值
def dangqian(HL, hhh):  # 当前行为可靠性 历史交互次数（阈值70）
    Rcurr = HL[19][0]
    if Rcurr > 0.5:
        if hhh <= 70 and hhh >= 0:
            g = 0.0001 * hhh * hhh + 0.5
        else:
            g = 1
        return 0.5 + g * (Rcurr - 0.5)
    else:
        return 0


# 计算历史信任值
def lishi(HL):  # 历史交互信息表（部分）
    hist = 0
    for i in range(19):
        hist += HL[i][0] * (math.pow(2, -(19 - i)))
    return hist


# 计算直接信任值
def zhijie(dqvalue, lsvalue, hhh, Scurr, HL, Thist):  # 当前信任值 历史信任值 历史交互次数 当前行为稳定性 历史交互信息表（部分） 历史信任值
    if hhh > 1:
        shuxi = 1 - (1 / (pow((math.exp(hhh - 1)), 0.1) + 1))
    else:
        shuxi = 0
    whist = shuxi * Scurr
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
        return ((whist * lsvalue + wcurr * dqvalue) - Thist) * n + Thist
    elif Rcurr <= 0.5:
        return whist * lsvalue + wcurr * dqvalue


# 计算推荐信任度
def tuijian(RL):  # 推荐信息表（部分）
    HR = 0
    jiahe = 0
    for i in range(20):
        HR += RL[i][0]
    if HR == 0:  # 如果没有推荐服务器
        return 0
    else:
        for i in range(20):
            jiahe += (RL[i][0] / HR) * RL[i][1]
    return jiahe


# 计算综合信任度
def zonghe(tjvalue, zjvalue, HHH, RL, id):  # 推荐信任度 直接信任度 历史交互次数列表 推荐信息列表 节点id
    if sum(HHH) == 0:
        a = 0
    else:
        a = HHH[id] / (sum(HHH) / 100)
    addR = []
    for i in range(100):
        RRR = 0
        for j in range(20):
            RRR += RL[i][j][0]
        addR.append(RRR)
    if sum(addR) == 0:
        b = 0
    else:
        b = addR[id] / (sum(addR) / 100)
    if a == 0 and b == 0:
        wr = 0
    elif a == 0 and b != 0:
        wr = 0.5
    else:
        wr = b / (a + b)
    wd = 1 - wr
    return wr * tjvalue + wd * zjvalue


# 计算综合信任度整体函数
def hanshhu(R, listhhh, listHL, listRL, listThist, S, id):  # 当前行为可靠性 历史交互次数（列表） 历史交互信息表（列表） 推荐信息表（列表） 行为稳定性 节点id
    Tcurr = dangqian(listHL[id], listhhh[id])  # 当前信任值
    Thist = lishi(listHL[id])  # 历史信任值
    Tzhijie = zhijie(Tcurr, Thist, listhhh[id], S, listHL[id], listThist[id])  # 直接信任值
    Ttuijian = tuijian(listRL[id])  # 推荐信任度
    TTT = zonghe(Ttuijian, Tzhijie, listhhh, listRL, id)  # 综合信任度
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
list_hhh = []
for i in range(100):
    list_hhh.append(0)

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
            # list_hhh[i] += 1
            # for gengxin in range(20):
            #     tuijian_result = 0
            #     tuijian_k1 = 1
            #     tuijian_HL = [[[0.5, 0.5]]]  # 推荐服务器 历史交互表
            #     for nn in range(19):
            #         tuijian_HL[0].append([0.5, 0.5])
            #     for ll in range(99):
            #         tuijian_HL.append([[0, 0]])
            #         for nn in range(19):
            #             tuijian_HL[tuijian_k1].append([0, 0])
            #         tuijian_k1 += 1
            #     tuijian_k2 = 0
            #     tuijian_RL = []  # 推荐服务器 推荐信息表
            #     for nn in range(100):
            #         tuijian_RL.append([[0, 0]])
            #         for ll in range(19):
            #             tuijian_RL[tuijian_k2].append([0, 0])
            #         tuijian_k2 += 1
            #     tuijian_hhh = []  # 推荐服务器 历史交互次数
            #     for ll in range(100):
            #         tuijian_hhh.append(0)
            #     tuijian_Thist = []  # 推荐服务器  历史信任值
            #     tuijian_Thist.append(0.5)
            #     list_RL[i][gengxin][0] = random.randint(0, 100)  # 随机产生推荐服务器与节点的历史交互次数
            #     for jisuan in range(list_RL[i][gengxin][0]):  # 以实际交互为准
            #         tuijian_add = 0
            #         tuijian_p = Node(2, list_Thist[i])
            #         tuijian_p.behav2()
            #         tuijian_HL[0].append([tuijian_p.R, 0])
            #         del tuijian_HL[0][0]
            #         for j in range(19):
            #             tuijian_add += abs(tuijian_HL[0][j + 1][0] - tuijian_HL[0][j][0])
            #         tuijian_S = tuijian_add / 19
            #         tuijian_HL[0][19][1] = tuijian_S
            #         tuijian_hhh[0] += 1  # 更新历史交互次数列表
            #         tuijian_zjhist=zhijie(dangqian(tuijian_HL[0], tuijian_hhh[0]), lishi(tuijian_HL[0]), tuijian_hhh[0], tuijian_HL[0][19][1], tuijian_HL[0],tuijian_Thist[0])
            #         tuijian_result = hanshhu(tuijian_p.R, tuijian_hhh, tuijian_HL, tuijian_RL, tuijian_Thist,tuijian_S, 0)
            #         tuijian_Thist[0]=tuijian_zjhist
            #     list_RL[i][gengxin][1] = tuijian_result
            # zjhist=zhijie(dangqian(list_HL[i], list_hhh[i]), lishi(list_HL[i]), list_hhh[i], list_HL[i][19][1], list_HL[i],list_Thist[i])
            # result = hanshhu(p.R, list_hhh, list_HL, list_RL, list_Thist, list_HL[i][19][1], i)
            # print('{},{},{},{},{},{}'.format(circul+1,dangqian(list_HL[i], list_hhh[i]),lishi(list_HL[i]),zjhist,tuijian(list_RL[i]),result),file=f)
            # # print(list_HL[i], file=f)
            # print(list_RL[i], file=f)
            # print('S {} ;    dqhist {} ;    Rcurr: {} ;'.format(list_HL[i][19][1],list_Thist[i],p.R), file=f)
            # print('dq: {}'.format(dangqian(list_HL[i], list_hhh[i])),file=f)
            # print('ls: {}'.format(lishi(list_HL[i])),file=f)
            # print('zj: {}'.format(zjhist),file=f)
            # print('tj: {}'.format(tuijian(list_RL[i])),file=f)
            # print('T：{} '.format(result),file=f)
            # list_Thist[i] = zjhist

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
            list_hhh[i] += 1

            # 更新推荐列表
            for gengxin in range(20):
                tuijian_result = 0
                tuijian_k1 = 1
                tuijian_HL = [[[0.5, 0.5]]]  # 推荐服务器 历史交互表
                for nn in range(19):
                    tuijian_HL[0].append([0.5, 0.5])
                for ll in range(99):
                    tuijian_HL.append([[0, 0]])
                    for nn in range(19):
                        tuijian_HL[tuijian_k1].append([0, 0])
                    tuijian_k1 += 1
                tuijian_k2 = 0
                tuijian_RL = []  # 推荐服务器 推荐信息表
                for nn in range(100):
                    tuijian_RL.append([[0, 0]])
                    for ll in range(19):
                        tuijian_RL[tuijian_k2].append([0, 0])
                    tuijian_k2 += 1
                tuijian_hhh = []  # 推荐服务器 历史交互次数
                for ll in range(100):
                    tuijian_hhh.append(0)
                tuijian_Thist = []  # 推荐服务器  历史信任值
                tuijian_Thist.append(0.5)
                list_RL[i][gengxin][0] = random.randint(0, 100)  # 随机产生推荐服务器与节点的历史交互次数
                for jisuan in range(list_RL[i][gengxin][0]):  # 以实际交互为准
                    tuijian_add = 0
                    if count4[jisuan] == 1:
                        tuijian_p = Node(1, list_Thist[i])
                        tuijian_p.behav1()
                        tuijian_HL[0].append([tuijian_p.R, 0])
                        del tuijian_HL[0][0]
                        for j in range(19):
                            tuijian_add += abs(tuijian_HL[0][j + 1][0] - tuijian_HL[0][j][0])
                        tuijian_S = tuijian_add / 19
                        tuijian_HL[0][19][1] = tuijian_S
                        tuijian_hhh[0] += 1  # 更新历史交互次数列表
                        tuijian_zjhist = zhijie(dangqian(tuijian_HL[0], tuijian_hhh[0]), lishi(tuijian_HL[0]),
                                                tuijian_hhh[0], tuijian_HL[0][19][1], tuijian_HL[0], tuijian_Thist[0])
                        tuijian_result = hanshhu(tuijian_p.R, tuijian_hhh, tuijian_HL, tuijian_RL, tuijian_Thist,
                                                 tuijian_S, 0)
                        tuijian_Thist[0] = tuijian_zjhist
                    elif count4[jisuan] == 0:
                        tuijian_p = Node(2, list_Thist[i])
                        tuijian_p.behav2()
                        tuijian_HL[0].append([tuijian_p.R, 0])
                        del tuijian_HL[0][0]
                        for j in range(19):
                            tuijian_add += abs(tuijian_HL[0][j + 1][0] - tuijian_HL[0][j][0])
                        tuijian_S = tuijian_add / 19
                        tuijian_HL[0][19][1] = tuijian_S
                        tuijian_hhh[0] += 1  # 更新历史交互次数列表
                        tuijian_zjhist = zhijie(dangqian(tuijian_HL[0], tuijian_hhh[0]), lishi(tuijian_HL[0]),
                                                tuijian_hhh[0], tuijian_HL[0][19][1], tuijian_HL[0], tuijian_Thist[0])
                        tuijian_result = hanshhu(tuijian_p.R, tuijian_hhh, tuijian_HL, tuijian_RL, tuijian_Thist,
                                                 tuijian_S, 0)
                        tuijian_Thist[0] = tuijian_zjhist
                list_RL[i][gengxin][1] = tuijian_result
            zjhist = zhijie(dangqian(list_HL[i], list_hhh[i]), lishi(list_HL[i]), list_hhh[i], list_HL[i][19][1],
                            list_HL[i], list_Thist[i])
            result = hanshhu(p.R, list_hhh, list_HL, list_RL, list_Thist, list_HL[i][19][1], i)
            print('{},{},{},{},{},{}'.format(circul + 1, dangqian(list_HL[i], list_hhh[i]), lishi(list_HL[i]), zjhist,
                                             tuijian(list_RL[i]), result), file=f)
            list_Thist[i] = zjhist

        # print('\n',file=f)


if __name__ == '__main__':
    with open('C:\\Users\\12549\\Desktop\\fout.txt', 'w') as f:
        main(f)
