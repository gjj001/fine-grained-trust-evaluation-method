import random
import math

class Node:
    '''
    定义一个节点类
    '''
    R=0
    S=0
    def __init__(self,behavior,value,h,recomserver):
        '''
        初始化节点属性
        :param behavior: 节点行为序号，1为行为1，2为行为2，3为行为3，4为行为4
        :param value: 节点信任值
        :param h: 节点与服务器历史交互次数
        :param recomserver: 推荐服务器数量
        '''
        self.behavior=behavior
        self.value=value
        self.h=h
        self.recomserver=recomserver
        pass
    def behav1(self,f):
        '''
        行为1：良好参与方，在服务器交互过程中保持正常稳定服务
              异常信息acc在0.5-1之间
              时延信息d在0-0.5之间
        :return:
        '''
        acc=[]
        d=[]
        sum=0
        for i in range(10):
            acc.append(random.randint(5000,10000)/10000)
            d.append(random.randint(0,5000)/10000)
            pass
        abnormal_factor=ACC(acc)
        delay_factor=calculate_delay_factor(d)
        self.R=(1/(1+math.exp(-abnormal_factor)))*delay_factor
        for i in range(10):
            if i<9:
                sum+=abs(acc[i+1]-acc[i])
            else:
                break
        self.S=sum/9
        print('异常信息 acc : {}'.format(acc), file=f)
        print('异常因子 abnormal_factor : {}'.format(abnormal_factor), file=f)
        print('时延信息 d : {}'.format(d), file=f)
        print('时延因子 delay_factor : {}'.format(delay_factor), file=f)
        print('行为可靠性 R : {}'.format(self.R), file=f)
        print('行为稳定性 S : {}'.format(self.S), file=f)
        pass
    def behav2(self, f):
        '''
        行为2：恶意参与方，行为一直差
              异常信息acc在0-0.5之间
              时延信息d在0.5-1之间
        :return:
        '''
        acc=[]
        d=[]
        sum=0
        for i in range(10):
            acc.append(random.randint(0,5000)/10000)
            d.append(random.randint(5000,10000)/10000)
            pass
        abnormal_factor = ACC(acc)
        delay_factor = calculate_delay_factor(d)
        self.R=(1/(1+math.exp(-abnormal_factor)))*delay_factor
        for i in range(10):
            if i<9:
                sum+=abs(acc[i + 1]-acc[i])
            else:
                break
        self.S=sum/9
        print('异常信息 acc : {}'.format(acc), file=f)
        print('异常因子 abnormal_factor : {}'.format(abnormal_factor), file=f)
        print('时延信息 d : {}'.format(d), file=f)
        print('时延因子 delay_factor : {}'.format(delay_factor), file=f)
        print('行为可靠性 R : {}'.format(self.R), file=f)
        print('行为稳定性 S : {}'.format(self.S), file=f)
        pass
    def behav3(self):
        '''
        行为3：恶意参与方，行为稳定性差，周期性的交替表现为良好行为和恶意行为
              假设一次异常度信息和时延信息为行为1
              一次异常度信息和时延信息为行为2
        :return:
        '''
        acc=[]
        d=[]
        sum=0
        for i in range(10):
            if i%2==0:
                acc.append(random.randint(5000,10000)/10000)
                d.append(random.randint(0,5000)/10000)
            else:
                acc.append(random.randint(0,5000)/10000)
                d.append(random.randint(5000,10000)/10000)
        abnormal_factor=ACC(acc)
        delay_factor=calculate_delay_factor(d)
        self.R=(1/(1+math.exp(-abnormal_factor)))*delay_factor
        for i in range(10):
            if i<9:
                sum+=abs(acc[i+1]-acc[i])
            else:
                break
        self.S=sum/9
        print('异常信息 acc : {}'.format(acc), file=f)
        print('异常因子 abnormal_factor : {}'.format(abnormal_factor), file=f)
        print('时延信息 d : {}'.format(d), file=f)
        print('时延因子 delay_factor : {}'.format(delay_factor), file=f)
        print('行为可靠性 R : {}'.format(self.R), file=f)
        print('行为稳定性 S : {}'.format(self.S), file=f)
        pass
    def behav4(self):
        '''
        行为4：恶意参与方，刚开始行为良好，让自己保持在一个较高水平的信任值下，进行恶意行为
        后又行为良好，信任值积累到一定程度之后，再进行恶意行为。即间断性的进行攻击
        :return:
        '''
        pass

class Server:
    '''
    定义一个服务器类，直接计算得到节点的间接信任值
    '''
    Text=0
    def __init__(self,amount):
        '''
        :param amount: 推荐服务器数量
        '''
        self.amount=amount
    def way1(self, f):
        '''
        方式1：对良好节点的推荐信任值高 0.5-1之间
              节点与推荐服务器的交互次数 0-50之间
        :return:
        '''
        valuelist=[]
        h_Server=[]
        h_all=0
        for i in range(self.amount):
            valuelist.append(random.randint(5000,10000)/10000)
            h_Server.append(random.randint(0,50))
            h_all+=h_Server[i]
        for i in range(self.amount):
            self.Text+=(h_Server[i]/h_all)*valuelist[i]
        print('推荐信任值集合：{}'.format(valuelist), file=f)
        print('对应推荐服务器历史交互次数：{}'.format(h_Server), file=f)
        print('间接信任值：{}'.format(self.Text), file=f)
        pass
    def way2(self, f):
        '''
        方式2：对恶意节点的推荐信任值低 -1--0.5之间
              节点与推荐服务器的交互次数0-50之间
        :return:
        '''
        valuelist=[]
        h_Server=[]
        h_all=0
        for i in range(self.amount):
            valuelist.append(random.randint(-10000,-5000)/10000)
            h_Server.append(random.randint(0, 50))
            h_all += h_Server[i]
        for i in range(self.amount):
            self.Text+=(h_Server[i]/h_all)*valuelist[i]
        print('推荐信任值集合：{}'.format(valuelist), file=f)
        print('对应推荐服务器历史交互次数：{}'.format(h_Server), file=f)
        print('间接信任值：{}'.format(self.Text), file=f)
        pass
    def way3(self, f):
        '''
        方式3：推荐信任值有低有高，假设一半高一半低
              节点与推荐服务器的交互次数0-50之间
        :return:
        '''
        valuelist=[]
        h_Server=[]
        h_all=0
        for i in range(self.amount):
            if i%2==0:
                valuelist.append(random.randint(0,10000)/10000)
            else:
                valuelist.append(random.randint(-10000,0)/10000)
            h_Server.append(random.randint(0, 50))
            h_all += h_Server[i]
        for i in range(self.amount):
            self.Text+=(h_Server[i]/h_all)*valuelist[i]
        print('推荐信任值集合：{}'.format(valuelist), file=f)
        print('对应推荐服务器历史交互次数：{}'.format(h_Server), file=f)
        print('间接信任值：{}'.format(self.Text), file=f)
        pass


#1、定义函数，计算异常因子
def ACC(list):
    xx=0
    for i in range(10):
        xx+=pow(list[i],i+1)*pow(0.8,10-i)
    abnormal_factor=1-math.exp(-xx)
    return abnormal_factor

#2、定义函数，计算时延因子
def calculate_delay_factor(list):
    yy=0
    for i in range(10):
        yy+=pow(list[i],i+1)*pow(0.8,10-i)
    delay_factor=math.exp(-yy)
    return delay_factor

#3、定义函数，计算时间衰减因子，参数t是当前时间，t0是最后一次信任建立更新时间
#时间抽象为周期数
def timeDecay(t,t0):
    return pow(2,-(t-t0))
    pass

#4、定义函数，计算熟悉度，参数是交互次数
def famil(h):
    if h==0:
        return 0
    elif h>=1:
        return 1-(1/(pow(math.exp(h-1),0.5)+1))
    pass

#5、定义函数，计算稳定性度量权重因子，参数是节点的历史行为稳定性S的集合和历史交互次数
def q(Node,h):
    S_all=0
    S_all+=Node.S
    Save=S_all/(h+1) #h+1目的保证分母不为0
    return Save
    pass

#6、定义函数，计算交互满意度，参数是稳定性和可靠性，假设稳定性和可靠性的权重参数都为0.5
def interSatis(Node):
    if Node.R==-1 or Node.S==-1:
        return -1
    else:
        return 0.5*Node.R+0.5*Node.S
    pass

#7、定义函数，计算直接信任值，参数：1、历史信任值 2、历史交互次数
def dirvalue(Node,Thist,h,t,t0):
    if Thist==-1:
        Tint=-1
        return Tint
    else:
        #r为历史信任值所占权重大小
        #g为实际当前交互满意度
        #历史交互次数阈值为1/pow(2*0.002,0.5)
        r=famil(h)*timeDecay(t,t0)*q(Node,h)
        if h>=0 and h<=(1/pow(2*0.002,0.5)):
            g=interSatis(Node)*(0.002*pow(h,2)+0.5)
        else:
            g=interSatis(Node)
        Tint=Thist*r+g*(1-r)
        return Tint

#8、定义函数，计算最终信任值 参数1、直接信任值Tint 2、间接信任值Text 3、归一化历史交互次数 4、归一化推荐服务器个数
def value(Tint,Text,h_Normalize,amount_Normalize):
    den=h_Normalize+amount_Normalize
    if h_Normalize==0 and amount_Normalize!=0:
        TTT=Text
    elif h_Normalize!=0 and amount_Normalize==0:
        TTT=Tint
    else:
        TTT=(amount_Normalize/den)*Text+(h_Normalize/den)*Tint
    return TTT

#9、定义函数，归一化处理，参数为列表
def normalize(list):
    deal=[]
    maxx=max(list)
    minn=min(list)
    mid=maxx-minn
    for i in range(len(list)):
        deal.append((list[i]-minn)/mid)
    return deal

def main(f):
    # 模拟联邦学习
    # for循环共进行20个周期，每个周期进行10轮迭代
    # 存储1-100节点历史交互次数
    list_interaction_counts = []
    for i in range(100):
        list_interaction_counts.append(0)
    # 存储1-100节点历史信任值
    list_Thist = []
    for i in range(100):
        list_Thist.append(0)
    recomnum = 50
    mark1 = 0
    mark2 = 1
    Storage_behavior_stability = [0]  # 存储行为稳定性
    for circul in range(20):
        print('第{}个周期'.format(circul + 1), file=f)
        print('-' * 80, file=f)
        # 每个周期100个节点全部作为参与者参与联邦学习
        # 100个节点中：1-40 行为1; 40-60 行为2; 60-80 行为3; 80-100 行为4;
        # 初始化节点类
        for i in range(100):
            print('{} ***'.format(i + 1), file=f)
            # 行为1
            if i + 1 < 40:
                p = Node(1, 0, list_interaction_counts[i], recomnum)  # 行为 信任值 历史交互次数 推荐服务器数量
                p.behav1(f)  # 行为稳定性和行为可靠性
                server = Server(recomnum)
                server.way1(f)  # 间接信任度
                Text = server.Text
                Tint = dirvalue(p, list_Thist[i], list_interaction_counts[i], 10, 8)  # 当前时间10，最后一次信任建立时间8  直接信任度
                print('直接信任值：{}'.format(Tint), file=f)
                TTT = value(Tint, Text, list_interaction_counts[i], recomnum)  # 最终信任度
                print('信任值：{}'.format(TTT), file=f)
                list_Thist[i] = TTT
                list_interaction_counts[i] += 1
            # 行为2
            elif i + 1 >= 40 and i + 1 < 60:
                p = Node(2, 0, list_interaction_counts[i], recomnum)
                p.behav2(f)
                server = Server(recomnum)
                server.way2(f)
                Text = server.Text
                Tint = dirvalue(p, list_Thist[i], list_interaction_counts[i], 10, 8)  # 当前时间10，最后一次信任建立时间8  直接信任度
                print('直接信任值：{}'.format(Tint), file=f)
                TTT = value(Tint, Text, list_interaction_counts[i], recomnum)  # 最终信任度
                print('信任值：{}'.format(TTT), file=f)
                list_Thist[i] = TTT
                list_interaction_counts[i] += 1
            # 行为3
            elif i + 1 >= 60 and i + 1 < 80:
                p = Node(3, 0, list_interaction_counts[i], recomnum)
                if mark1 % 2 == 0:
                    p.behav1(f)
                elif mark1 % 2 == 1:
                    p.behav2(f)
                server = Server(recomnum)
                server.way3(f)
                Text = server.Text
                Tint = dirvalue(p, list_Thist[i], list_interaction_counts[i], 10, 8)  # 当前时间10，最后一次信任建立时间8  直接信任度
                print('直接信任值：{}'.format(Tint), file=f)
                TTT = value(Tint, Text, list_interaction_counts[i], recomnum)  # 最终信任度
                print('信任值：{}'.format(TTT), file=f)
                list_Thist[i] = TTT
                list_interaction_counts[i] += 1
            # 行为4
            else:
                p = Node(4, 0, list_interaction_counts[i], recomnum)
                if mark2 % 5 == 0:
                    p.behav2(f)
                else:
                    p.behav1(f)
                server = Server(recomnum)
                server.way3(f)
                Text = server.Text
                Tint = dirvalue(p, list_Thist[i], list_interaction_counts[i], 10, 8)  # 当前时间10，最后一次信任建立时间8  直接信任度
                print('直接信任值：{}'.format(Tint), file=f)
                TTT = value(Tint, Text, list_interaction_counts[i], recomnum)  # 最终信任度
                print('信任值：{}'.format(TTT), file=f)
                list_Thist[i] = TTT
                list_interaction_counts[i] += 1

        mark1 += 1
        mark2 += 1
        print('\n', file=f)
        pass

if __name__ == '__main__':
    with open('C:\\Users\\tsy\\Desktop\\fout.txt', 'w') as f:
        main(f)