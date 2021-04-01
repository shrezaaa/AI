from collections import deque

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
        return 1


class Interval:
    def __init__(self, id, demand):
        self.intervalID = int(id)
        self.intervalDemand = int(demand)


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


def main() :
    readFilesAndCreateObjects()





main()