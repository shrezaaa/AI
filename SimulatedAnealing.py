from collections import deque
import secrets
from random import random
import math

global unitCounts
global intervalCounts

global unitArray
unitArray = []

global intervalsArray
intervalsArray = []

global orderList
orderList = []

class Unit:
    def __init__(self, id, capacity, repairCount,intervalsCount):
        self.unitID = int(id)
        self.unitCapacity = int(capacity)
        self.unitRepairCount = int(repairCount)
        self.unitPools = self.genreatePools(self.unitRepairCount,intervalsCount)

    def genreatePools(self,reapirCount,intervals):
        pools = []
        tempArray = []
        for x in range(reapirCount):
            tempArray.append(1)
        for x in range(intervals-reapirCount):
            tempArray.append(0)

        pools.append(tempArray)
        items = deque(tempArray)
        for x in range(intervals-reapirCount):
            items.rotate(1)
            pools.append(list(items))
        # print(pools)
        return pools


class Interval:
    def __init__(self, id, demand):
        self.intervalID = int(id)
        self.intervalDemand = int(demand)

class solution:
    def __init__(self,orderList:list,demand:int):
        self.orderList = orderList
        self.demand = demand

class Solution:
    def __init__(self,orderList:list,minimumExtraCapacity:int):
        self.orderList = orderList
        self.minimumExtraCapacity = minimumExtraCapacity

def readFilesAndCreateObjects():
    secondFile = open("second.txt", 'rt')
    lines = secondFile.read().split('\n')
    intervalCounts = int(lines.pop(0))
    for line in lines:
        res = line.split(',')
        intervalsArray.append(Interval(res[0], res[1]))
    secondFile.close()

    firstFile = open("first.txt", "rt")
    lines = firstFile.read().split('\n')
    unitCounts = int(lines.pop(0))
    for line in lines:
        res = line.split(',')
        unitArray.append(Unit(res[0], res[1], res[2], intervalCounts))
    firstFile.close()

def calcIntervalExtraCapacity(orderList:[],intervalIndex:int):
    sum = 0
    for index in range(len(unitArray)):
        if orderList[index][intervalIndex] == 0 :
            sum = sum + unitArray[index].unitCapacity
    return sum - intervalsArray[intervalIndex].intervalDemand


def acceptanceProbability(currentMinimumExtraCapacity,neighbourMinimumExtraCapacity,temp):
    if neighbourMinimumExtraCapacity > currentMinimumExtraCapacity :
        return 1.0
    # print(((neighbourDemand - currentDemand)/temp))
    # return ((neighbourDemand - currentDemand)/temp)
    return 0

def fillOrders():
    orderList = []
    for unit in unitArray:
        orderList.append(secrets.choice(unit.unitPools))
    print(orderList)
    return orderList


def calcDemandsInOrders(orderList):
    demand = 0
    for index in range(len(intervalsArray)):
        extraCapacity = calcIntervalExtraCapacity(orderList,index)
        if extraCapacity < 0 :
            demand = demand + extraCapacity
        print(str(index) + " extra capacity is " + str((calcIntervalExtraCapacity(orderList,index))))
    return demand

def findMinimumIntervalCapacityInOrders(orderList):
    minimum = calcIntervalExtraCapacity(orderList,0)
    minimumInterval:int
    minimumIntervalsList = []
    for index in range(len(intervalsArray)):
        extraCapacity = calcIntervalExtraCapacity(orderList,index)
        if extraCapacity < minimum :
            minimum = extraCapacity
            minimumInterval = index
            minimumIntervalsList = []
        elif extraCapacity == minimum :
            minimumIntervalsList.append(index)
    if len(minimumIntervalsList)!=0:
        minimumIntervalsList.append(minimumInterval)
        minimumInterval = secrets.choice(minimumIntervalsList)
    return minimumInterval

def findNeighbourOrderList(orderList):
    newOrder = orderList.copy()
    minimumInterval = findMinimumIntervalCapacityInOrders(orderList);
    print(minimumInterval)
    disabledUnits= []
    for unitIndex in range(len(orderList)):
        if orderList[unitIndex][minimumInterval] == 1:
            disabledUnits.append(unitIndex)
    print(disabledUnits)
    if len(disabledUnits)!=0:
        selectedUnit = secrets.choice(disabledUnits)
        selectableUnitPools=[]
        print(selectedUnit)

    for unitPool in unitArray[selectedUnit].unitPools:
        if unitPool[minimumInterval] == 0:
            selectableUnitPools.append(unitPool)
    if len(selectableUnitPools)!=0:
        selectedUnitPool = secrets.choice(selectableUnitPools)
        print(selectedUnitPool)
        newOrder[selectedUnit] = selectedUnitPool
    minimumInterval = findMinimumIntervalCapacityInOrders(newOrder);
    minimumValue = calcIntervalExtraCapacity(newOrder,minimumInterval)

    solution = Solution(newOrder,minimumValue)
    return solution

def main() :
    readFilesAndCreateObjects()
    orderList = fillOrders()
    minimumInterval = findMinimumIntervalCapacityInOrders(orderList);
    minimumValue = calcIntervalExtraCapacity(orderList, minimumInterval)
    currentSolution = Solution(orderList,minimumValue)
    print(currentSolution.orderList)
    print(calcDemandsInOrders(currentSolution.orderList))
    print()
    temp = 1000
    colingRate = 200

    while(temp > 1 ):
        # orderList = fillOrders()
        # demand = calcDemandsInOrders(orderList)
        # newSolution = solution(orderList,demand)
        # if acceptanceProbability(currentSolution.demand,newSolution.demand,temp) > random():
        #     print('true')
        #     currentSolution = newSolution

        newSolution = findNeighbourOrderList(currentSolution.orderList)
        print(newSolution.orderList)
        print(calcDemandsInOrders(newSolution.orderList))
        if acceptanceProbability(currentSolution.minimumExtraCapacity,newSolution.minimumExtraCapacity,temp) > random():
            print('true')
            currentSolution = newSolution
        print()
        temp = temp - colingRate

    # soooo this is solution
    print()
    print("answer is")
    print(currentSolution.orderList)
    print(calcDemandsInOrders(orderList))
    print("Minimum Extra is " + str(currentSolution.minimumExtraCapacity))
    # print(findMinimumIntervalCapacityInOrders(currentSolution.orderList))
    # findNeighbourOrderList(currentSolution.orderList)
main()