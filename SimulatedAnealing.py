

class Unit:
    def __init__(self, id, capacity, repairCount):
        self.unitID = id
        self.unitCapacity = capacity
        self.unitRepairCount = repairCount
        self.unitPools = self.genreatePools()

    def genreatePools(self):
        return


class Interval:
    def __init__(self, id, demand):
        self.intervalID = id
        self.intervalDemand = demand


class order:
    def generate_period_unit_states(period_count: int, period_works_count: int):
        state_list = []
        for i in range(pow(2, period_count)):
            state = bin(i)[2:]
            state = str(0) * (period_count - len(state)) + state
            if state.count('1') == period_works_count and state.contains(str(1) * period_works_count):
                state_list.append(state)
        return state_list

