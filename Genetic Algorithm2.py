from collections import deque
import secrets
from random import randrange
from random import random

import math

global unitCounts
global intervalCounts

global unitArray
unitArray = []

global intervalsArray
intervalsArray = []

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

class Population:
    def __init__(self,size,initialize):
        self.size = size
        self.individulas = [None] * size
        if initialize=='true':
            for i in range(size):
                indiv = generateIndividual()
                self.individulas[i] = indiv
                self.saveIndividual(i,indiv)

    def saveIndividual(self,index,indiv):
        self.individulas[index] = indiv

    def getIndividual(self,i):
        return self.individulas[i]

    # tested
    def getFittestInPop(self):
        fittest = self.individulas[0]
        for i in range(len(self.individulas)):
            if self.findMinimumIntervalCapacityInOrders(fittest) <= self.findMinimumIntervalCapacityInOrders(self.individulas[i]):
                fittest = self.individulas[i]
        return fittest

    def getFittestFitnessRate(self):
        fit = self.getFittestInPop()
        return self.findMinimumIntervalCapacityInOrders(fit)

    # tested
    def findMinimumIntervalCapacityInOrders(self,orderList):
        minimumInterval = -1
        minimum = self.calcIntervalExtraCapacity(orderList, 0)
        minimumIntervalsList = []
        for intervalIndex in range(len(intervalsArray)):
            extraCapacity = self.calcIntervalExtraCapacity(orderList, intervalIndex)
            if extraCapacity < minimum:
                minimum = extraCapacity
                minimumInterval = intervalIndex
                minimumIntervalsList = []
            elif extraCapacity == minimum:
                minimumIntervalsList.append(intervalIndex)
        if len(minimumIntervalsList) != 0:
            if minimumInterval > -1:
                minimumIntervalsList.append(minimumInterval)
            minimumInterval = secrets.choice(minimumIntervalsList)
        minimumIntervalsList = []
        # return minimumInterval
        return self.calcIntervalExtraCapacity(orderList, minimumInterval)

    # tested
    def calcIntervalExtraCapacity(self,orderList: [], intervalIndex: int):
        sum = 0
        for unitIndex in range(len(unitArray)):
            if orderList[unitIndex][intervalIndex] == 0:
                sum = sum + unitArray[unitIndex].unitCapacity
        return sum - intervalsArray[intervalIndex].intervalDemand

    # for test
    def calcAllNeededInOrders(self,orderList):
        neededCapcacity = 0
        for index in range(len(intervalsArray)):
            extraCapacity = self.calcIntervalExtraCapacity(orderList, index)
            if extraCapacity < 0:
                neededCapcacity = neededCapcacity + extraCapacity
            print(str(index) + " & Extra Capacity is " + str(
                (self.calcIntervalExtraCapacity(orderList, index))))
        return neededCapcacity   ##  #



class Algorithm:
    def __init__(self,uniformRate,mutationRate,tournamentSize,elitism):
        self.uniformRate = uniformRate
        self.mutationRate = mutationRate
        self.tournamentSize = tournamentSize
        self.elitism = elitism

    def evelopePopulation(self,pop:Population):
        newPopulation = Population(pop.size,'false')

        # keep the best
        if self.elitism=='true':
            newPopulation.saveIndividual(0,pop.getFittestInPop())

        # crossover Population
        if self.elitism=='true':
            self.elitismOffset = 1
        else :
            self.elitismOffset = 0;

        #crossover

        for i in range(self.elitismOffset,pop.size,1):
            indiv1 = self.tournamentSelection(pop)
            indiv2 = self.tournamentSelection(pop)
            newIndiv = self.crossover(indiv1,indiv2)
            newPopulation.saveIndividual(i,newIndiv)
            # print(str(i) + " is")
            # printIndividuals(newIndiv)
        # print('changed')
        # printIndividuals(newPopulation.individulas)

        for i in range(self.elitismOffset,pop.size,1):
            mutatedIndiv = self.mutate(newPopulation.getIndividual(i))
            newPopulation.saveIndividual(i,mutatedIndiv)

        return newPopulation

    #  tested
    def crossover(self,indiv1,indiv2):
        newIndiv = [None] * len(indiv1)
        for i in range(len(indiv1)):
            if random() <= self.uniformRate:
                newIndiv[i] = indiv1[i]
            else:
                newIndiv[i] = indiv2[i]
        return newIndiv

    def mutate(self,indiv):
        for i in range(len(indiv)):
            if random() <=  self.mutationRate:
                randomGenePoll = secrets.choice(unitArray[i].unitPools)
                indiv[i] = randomGenePoll
        return indiv

    def tournamentSelection(self,pop:Population):
        tournomentPop = Population(self.tournamentSize,'false')
        for i in range(self.tournamentSize):
            randomID = randrange(pop.size)
            tournomentPop.saveIndividual(i,pop.getIndividual(randomID))

        fittest = tournomentPop.getFittestInPop()
        # print(tournomentPop.individulas[0])
        # print(tournomentPop.individulas[1])
        # print(self.crossover(tournomentPop.individulas[0],tournomentPop.individulas[1]))

        #  for test
        # print(tournomentPop.calcAllNeededInOrders(fittest))
        return fittest



def generateIndividual():
    individual = []
    for unit in unitArray:
        individual.append(secrets.choice(unit.unitPools))
    return individual

def printIndividuals(indivLists:list):
    for i in indivLists:
        print(i)


def printPop(pop:Population,number):
    print('pop test' + str(number))
    for i in range(len(pop.individulas)):
        print('indiv' + str(i))
        print(pop.calcAllNeededInOrders(pop.individulas[i]))
        print()

def main() :
    readFilesAndCreateObjects()
    pop = Population(10,'true')
    # printIndividuals(pop.individulas)

    # printPop(pop,1)

    # print(pop.getFittestInPop())
    # print(pop.getFittestFitnessRate())
    algorithm = Algorithm(0.5,0.015,5,'true')
    newPop = algorithm.evelopePopulation(pop)
    # print(algorithm.mutate(pop.individulas[9]))
    # algorithm.tournamentSelection(pop)
    # print(pop.getFittestInPop())
    # print(pop.calcAllNeededInOrders(pop.getFittestInPop()))

    generationCount = 100
    for generationIndex in range(generationCount):
        if pop.getFittestFitnessRate() <= newPop.getFittestFitnessRate():
            print("generation: "+ str(generationIndex) + " fittest: " + str(newPop.getFittestFitnessRate()))
            pop = newPop
        newPop = algorithm.evelopePopulation(pop)

    print()
    print('answer is')
    fittest = pop.getFittestInPop()
    print(fittest)
    print(pop.calcAllNeededInOrders(fittest))
    print("fittest fitness is: " + str(pop.getFittestFitnessRate()))

main()
