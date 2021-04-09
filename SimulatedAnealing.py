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

def calcIntervalExtraCapacity(orderList:[], intervalIndex:int):
    sum = 0
    for unitIndex in range(len(unitArray)):
        if orderList[unitIndex][intervalIndex] == 0 :
            sum = sum + unitArray[unitIndex].unitCapacity
    return sum - intervalsArray[intervalIndex].intervalDemand


def calcIntervalExactCapacity(orderList:[], intervalIndex:int):
    sum = 0
    for unitIndex in range(len(unitArray)):
        if orderList[unitIndex][intervalIndex] == 0 :
            sum = sum + unitArray[unitIndex].unitCapacity
    return sum

def acceptanceProbability(currentMinimumExtraCapacity,neighbourMinimumExtraCapacity,temp):
    if currentMinimumExtraCapacity < neighbourMinimumExtraCapacity :
        return 1.0
    print(math.exp((neighbourMinimumExtraCapacity - currentMinimumExtraCapacity)/temp))
    return math.exp((neighbourMinimumExtraCapacity - currentMinimumExtraCapacity)/temp)

def fillOrders():
    orderList = []
    for unit in unitArray:
        orderList.append(secrets.choice(unit.unitPools))
    return orderList


def calcAllNeededInOrders(orderList):
    neededCapcacity = 0
    for index in range(len(intervalsArray)):
        extraCapacity = calcIntervalExtraCapacity(orderList, index)
        if extraCapacity < 0 :
            neededCapcacity = neededCapcacity + extraCapacity
        print(str(index) +" Exact Capacity is "+ str(calcIntervalExactCapacity(orderList, index)) + " & Extra Capacity is " + str((calcIntervalExtraCapacity(orderList, index))))
    return neededCapcacity

def findMinimumIntervalCapacityInOrders(orderList):
    minimumInterval=-1
    minimum = calcIntervalExtraCapacity(orderList, 0)
    minimumIntervalsList = []
    for intervalIndex in range(len(intervalsArray)):
        extraCapacity = calcIntervalExtraCapacity(orderList, intervalIndex)
        if extraCapacity < minimum :
            minimum = extraCapacity
            minimumInterval = intervalIndex
            minimumIntervalsList = []
        elif extraCapacity == minimum :
            minimumIntervalsList.append(intervalIndex)
    if len(minimumIntervalsList)!=0:
        if minimumInterval > -1 :
            minimumIntervalsList.append(minimumInterval)
        minimumInterval = secrets.choice(minimumIntervalsList)
    minimumIntervalsList = []
    return minimumInterval

def findNeighbourOrderList(orderList,minimumInterval):
    newOrderList = orderList.copy()
    disabledUnits= []
    for unitIndex in range(len(newOrderList)):
        if newOrderList[unitIndex][minimumInterval] == 1:
            disabledUnits.append(unitIndex)
    selectableUnitPools=[]
    selectedUnit = secrets.choice(disabledUnits)

    if selectedUnit:
        for unitPool in unitArray[selectedUnit].unitPools:
            if unitPool[minimumInterval] == 0:
                selectableUnitPools.append(unitPool)
        if len(selectableUnitPools)!=0:
            selectedUnitPool = secrets.choice(selectableUnitPools)
            newOrderList[selectedUnit] = selectedUnitPool
    newMinimumInterval = findMinimumIntervalCapacityInOrders(newOrderList);
    minimumValue = calcIntervalExtraCapacity(newOrderList, newMinimumInterval)

    solution = Solution(newOrderList,minimumValue)
    return solution

def main() :
    readFilesAndCreateObjects()
    orderList = fillOrders()
    minimumInterval = findMinimumIntervalCapacityInOrders(orderList)
    minimumValue = calcIntervalExtraCapacity(orderList, minimumInterval)
    global currentSolution
    global bestSolution
    currentSolution = Solution(orderList,minimumValue)
    bestSolution = currentSolution
    print(currentSolution.orderList)
    print("all needed " + str(calcAllNeededInOrders(currentSolution.orderList)))
    print()

    temp = 1000
    colingRate = 10

    while(temp > 1 ):
        minimumInterval = findMinimumIntervalCapacityInOrders(currentSolution.orderList);
        newSolution = findNeighbourOrderList(currentSolution.orderList,minimumInterval)
        print(newSolution.orderList)
        print("all needed " + str(calcAllNeededInOrders(newSolution.orderList)))
        print("Minimum Extra is " + str(newSolution.minimumExtraCapacity))
        if acceptanceProbability(currentSolution.minimumExtraCapacity,newSolution.minimumExtraCapacity,temp) > random():
            print('true')
            currentSolution = newSolution

        if bestSolution.minimumExtraCapacity < newSolution.minimumExtraCapacity:
            bestSolution = newSolution

        print()
        temp = temp - colingRate

    # so this is answer solution
    print()
    print("answer is")
    print(bestSolution.orderList)
    print("all needed " + str(calcAllNeededInOrders(bestSolution.orderList)))
    print("Minimum Extra is " + str(bestSolution.minimumExtraCapacity))

main()