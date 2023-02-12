# -*- coding: utf-8 -*-

import random
import pandas
import numpy as np
import math
import matplotlib.pyplot as plt

class GAList(object):
    """
        类名：GAList
        类说明：	遗传算法类,一个GA类包含了一个种群,及其种群内的信息
    """

    def __init__(self, aCrossRate, aMutationRage, aUnitCount, aGeneLenght, aMatchFun=lambda: 1):
        """ 构造函数 """
        self.crossRate = aCrossRate  # 交叉概率 #
        self.mutationRate = aMutationRage  # 突变概率 #
        self.unitCount = aUnitCount  # 个体数 #
        self.geneLenght = aGeneLenght  # 基因长度 #
        self.matchFun = aMatchFun  # 适配函数
        self.population = []  # 种群
        self.best = None  # 保存这一代中最好的个体
        self.generation = 1  # 第几代 #
        self.crossCount = 0  # 交叉数量 #
        self.mutationCount = 0  # 突变个数 #
        self.bounds = 0.0  # 适配值之和，用于选择时计算概率
        self.initPopulation()  # 初始化种群 #

    def initPopulation(self):
        """
            函数名：initPopulation(self)
            函数功能：	随机初始化得到一个种群
                输入	1 	self：类自身
                输出	1	无
            其他说明：无
        """
        self.population = []
        unitCount = self.unitCount
        while unitCount > 0:
            gene = [x for x in range(self.geneLenght)]
            random.shuffle(gene)  # 随机洗牌 #
            unit = GAUnit(gene)
            self.population.append(unit)
            unitCount -= 1

    def judge(self):
        """
            函数名：judge(self)
            函数功能：	重新计算每一个个体单元的适配值
                输入	1 	self：类自身
                输出	1	无
            其他说明：无
        """
        self.bounds = 0.0
        self.best = self.population[0]
        for unit in self.population:
            unit.value = self.matchFun(unit)
            self.bounds += unit.value
            if self.best.value < unit.value:  # score为距离的倒数 所以越小越好 #
                self.best = unit

    def cross(self, parent1, parent2):
        """
            函数名：cross(self, parent1, parent2)
            函数功能：	根据parent1和parent2基于序列,随机选取长度为n的片段进行交换(n=index2-index1)
                输入	1 	self：类自身
                    2	parent1: 进行交叉的双亲1
                    3	parent2: 进行交叉的双亲2
                输出	1	newGene： 通过交叉后的一个新的遗传个体的基因序列号
            其他说明：进行交叉时采用的策略是,将parent2的基因段tempGene保存下来,然后对基因1所有序列号g依次进行判断,
                如果g在tempGene内,则舍去,否则就保存下来,并在第index1的位置插入tempGene
        """
        index1 = random.randint(0, self.geneLenght - 1)  # 随机生成突变起始位置 #
        index2 = random.randint(index1, self.geneLenght - 1)  # 随机生成突变终止位置 #
        tempGene = parent2.gene[index1:index2]  # 交叉的基因片段
        newGene = []
        p1len = 0
        for g in parent1.gene:
            if p1len == index1:
                newGene.extend(tempGene)  # 插入基因片段
                p1len += 1
            if g not in tempGene:
                newGene.append(g)
                p1len += 1
        self.crossCount += 1
        return newGene

    def mutation(self, gene):
        """
            函数名：mutation(self, gene)
            函数功能：	对输入的gene个体进行变异,也就是随机交换两个位置的基因号
                输入	1 	self：类自身
                    2	gene: 进行变异的个体基因序列号
                输出	1	newGene： 通过交叉后的一个新的遗传个体的基因序列
            其他说明：无
        """
        index1 = random.randint(0, self.geneLenght - 1)
        index2 = random.randint(0, self.geneLenght - 1)
        # 随机选择两个位置的基因交换--变异
        newGene = gene[:]  # 产生一个新的基因序列，以免变异的时候影响父种群
        newGene[index1], newGene[index2] = newGene[index2], newGene[index1]
        self.mutationCount += 1
        return newGene

    def getOneUnit(self):
        """
            函数名：getOneUnit(self)
            函数功能：	通过轮盘赌法,依据个体适应度大小,随机选择一个个体
                输入	1 	self：类自身
                输出	1	unit：所选择的个体
            其他说明：无
        """
        r = random.uniform(0, self.bounds)
        for unit in self.population:
            r -= unit.value
            if r <= 0:
                return unit

        raise Exception("选择错误", self.bounds)

    def newChild(self):
        """
            函数名：newChild(self)
            函数功能：	按照预定的概率进行交叉与变异后产生新的后代
                输入	1 	self：类自身
                输出	1	GAUnit(gene)：所产生的后代
            其他说明：无
        """
        parent1 = self.getOneUnit()
        rate = random.random()

        # 按概率交叉
        if rate < self.crossRate:  # 交叉
            parent2 = self.getOneUnit()
            gene = self.cross(parent1, parent2)
        else:  # 不交叉
            gene = parent1.gene

        # 按概率突变
        rate = random.random()
        if rate < self.mutationRate:
            gene = self.mutation(gene)

        return GAUnit(gene)

    def nextGeneration(self):
        """
            函数名：nextGeneration(self)
            函数功能：	产生下一代
                输入	1 	self：类自身
                输出	1	无
            其他说明：无
        """
        self.judge()
        newPopulation = []  # 新种群
        newPopulation.append(self.best)  # 把最好的个体加入下一代 #
        while len(newPopulation) < self.unitCount:
            newPopulation.append(self.newChild())
        self.population = newPopulation
        self.generation += 1


class GAUnit(object):
    """
        类名：GAUnit
        类说明：	遗传算法个体类
    """

    def __init__(self, aGene=None, SCORE_NONE=-1):
        """ 构造函数 """
        self.gene = aGene  # 个体的基因序列
        self.value = SCORE_NONE  # 初始化适配值


class TSP(object):
    def __init__(self, Position, Dist, CityNum):
        """ 构造函数 """
        self.citys = Position  # 城市坐标
        self.dist = Dist  # 城市距离矩阵
        self.citynum = CityNum  # 城市数量

        self.ga = GAList(aCrossRate=0.7,  # 交叉率
                         aMutationRage=0.02,  # 突变概率
                         aUnitCount=100,  # 一个种群中的个体数
                         aGeneLenght=self.citynum,  # 基因长度（城市数）
                         aMatchFun=self.matchFun())  # 适配函数

    def distance(self, path):
        """
            函数名：distance(self, path)
            函数功能：	根据路径求出总路程
                输入	1 	self：类自身
                输入 2	path：路径
                输出	1	无
            其他说明：无
        """
        # 计算从初始城市到最后一个城市的路程
        distance = sum([self.dist[city1][city2] for city1, city2 in
                        zip(path[:self.citynum], path[1:self.citynum + 1])])
        # 计算从初始城市到最后一个城市再回到初始城市所经历的总距离
        distance += self.dist[path[-1]][0]

        return distance

    def matchFun(self):
        """
            函数名：matchFun(self)
            函数功能：	定义适配函数,并返回函数句柄
                输入	1 	self：类自身
                输出	1	所定义的适配函数的函数句柄
            其他说明：无
        """
        return lambda life: 1.0 / self.distance(life.gene)

    def run(self, generate=0):
        """
            函数名：run(self, n=0)
            函数功能：	遗传算法解旅行商问题的运行函数
                输入	1 	self：类自身
                     2	generate：种群迭代的代数
                输出	1	distance:最小路程
                    2	self.ga.best.gene：最好路径
                    3	distance_list：每一代的最好路径列表
            其他说明：无
        """
        distance_list = []

        while generate > 0:
            self.ga.nextGeneration()
            distance = self.distance(self.ga.best.gene)
            distance_list.append(distance)
            generate -= 1

        return distance, self.ga.best.gene, distance_list


class Node:
    """
    类名：Node
    函数功能：	从外界读取城市数据并处理
        输入	无
        输出	1 Position：各个城市的位置矩阵
            2 CityNum：城市数量
            3 Dist：城市间距离矩阵
    其他说明：无
    """

    def __init__(self, CityNum):
        """
        函数名：GetData()
        函数功能：	从外界读取城市数据并处理
            输入	无
            输出	1 Position：各个城市的位置矩阵
                2 CityNum：城市数量
                3 Dist：城市间距离矩阵
        其他说明：无
        """
        self.visited = [False] * CityNum  # 记录城市是否走过
        self.start = 0  # 起点城市
        self.end = 0  # 目标城市
        self.current = 0  # 当前所处城市
        self.num = 0  # 走过的城市数量
        self.pathsum = 0  # 走过的总路程
        self.lb = 0  # 当前结点的下界
        self.listc = []  # 记录依次走过的城市


def GetData(datapath):
    """
    函数名：GetData()
    函数功能：	从外界读取城市数据并处理
        输入	无
        输出	1 Position：各个城市的位置矩阵
            2 CityNum：城市数量
            3 Dist：城市间距离矩阵
    其他说明：无
    """
    dataframe = pandas.read_csv(datapath, sep=" ", header=None,encoding='utf-8')
    Cities = dataframe.iloc[:, 1:3]
    Position = np.array(Cities)  # 从城市A到B的距离矩阵
    CityNum = Position.shape[0]  # CityNum:代表城市数量
    Dist = np.zeros((CityNum, CityNum))  # Dist(i,j)：城市i与城市j间的距离

    # 计算距离矩阵
    for i in range(CityNum):
        for j in range(CityNum):
            if i == j:
                Dist[i, j] = math.inf
            else:
                Dist[i, j] = math.sqrt(np.sum((Position[i, :] - Position[j, :]) ** 2))
    return Position, CityNum, Dist


def ResultShow(Min_Path, BestPath, CityNum, string):
    """
        函数名：GetData()
        函数功能：	从外界读取城市数据并处理
            输入	无
            输出	1 Position：各个城市的位置矩阵
                2 CityNum：城市数量
                3 Dist：城市间距离矩阵
        其他说明：无
    """
    print("基于" + string + "求得的旅行商最短路径为：")
    for m in range(CityNum):
        print(str(BestPath[m]) + "—>", end="")
    print(BestPath[CityNum])
    print("总路径长为：" + str(Min_Path))
    print()


def draw(BestPath, Position, title, flag=False, generate=0, distance_list=[]):
    """
        函数名：draw(BestPath,Position,title)
        函数功能：	通过最优路径将旅行商依次经过的城市在图表上绘制出来
            输入	1 	BestPath：最优路径
                2	Position：各个城市的位置矩阵
                3	title:图表的标题
            输出	无
        其他说明：无
    """
    plt.title(title)
    plt.plot(Position[:, 0], Position[:, 1], 'bo')
    for i, city in enumerate(Position):
        plt.text(city[0], city[1], str(i))
    plt.plot(Position[BestPath, 0], Position[BestPath, 1], color='red')
    plt.show()

    if flag:
        plt.plot(generate, distance_list)
        plt.xlabel('generation')
        plt.ylabel('distance')
        plt.title('generation--distance')
        plt.show()


if __name__ == '__main__':
    Position, CityNum, Dist = GetData("cities.csv")
    tsp = TSP(Position, Dist, CityNum)
    generate = 100
    Min_Path, BestPath, distance_list = tsp.run(generate)

    # 结果打印
    BestPath.append(BestPath[0])
    ResultShow(Min_Path, BestPath, CityNum, "GA")
    draw(BestPath, Position, "GA", True, range(generate), distance_list)
