import random
from itertools import combinations
import matplotlib.pyplot as plt
import numpy as np


class Genetic:

    units_data_dic = {}
    units_raw_data = {}
    intervals_raw_data = {}
    generations = {}
    fittness_list = []
    input_1_data = []
    input_2_data = []
    random_list = []
    numberOfChromosomes = 20
    Pc = 0.7
    Pm = 0.001
    generations_number = 100
    fitness_data_dic = {}

    def _init_(self, input_1, input_2):
        self.input_1 = input_1
        self.input_2 = input_2
        self.input_1_data = self.input_1.readlines()
        self.input_2_data = self.input_2.readlines()
        self.init_fitness_array()
        self.units_data_mapping()
        self.intervals_data_mapping()
        self.create_chromosome(self.numberOfChromosomes)
        self.check_min()
        self.iterate_generation()
        self.replace_with_min()
        self.plot_chart()

    def init_fitness_array(self):
        for i in range(int(self.input_2_data[0])):
            self.fitness_data_dic[i] = []

    def iterate_generation(self):
        for i in range(self.generations_number):
            self.calculate_fittness()
            self.roulette_wheel_selection()
            self.crossover()
            self.mutation()
            self.overwrite_generation()

    def binary_permutations(self, binary_list):
        for comb in combinations(range(len(binary_list)), binary_list.count(1)):
            result = [0] * len(binary_list)
            for i in comb:
                result[i] = 1
            if binary_list.count(1) > 1:
                count = 0
                max_ones = 0
                for i in range(0, len(result)):
                    if (result[i] == 0):
                        count = 0
                    else:
                        count += 1
                        max_ones = max(max_ones, count)
                if max_ones == binary_list.count(1):
                    yield result
            else:
                yield result

    def calculate_permutation(self, resting_count, year_range):
        temp_array = []
        for i in range(int(year_range)):
            if resting_count != 0:
                temp_array.append(1)
                resting_count -= 1
            else:
                temp_array.append(0)

        return self.binary_permutations(temp_array)

    def units_data_mapping(self):
        counter = 0
        temp_array = []

        for line in self.input_1_data[1:]:
            temp_array.append(int(line))
            counter += 1
            if counter % 3 == 0:
                self.units_raw_data[int(counter / 3 - 1)] = temp_array
                temp_array = []

        for i in range(int(self.input_1_data[0])):
            self.units_data_dic[i + 1] = list(self.calculate_permutation(
                self.units_raw_data[i][2], self.input_2_data[0]))

    def intervals_data_mapping(self):
        counter = 0
        temp_array = []

        for line in self.input_2_data[1:]:
            temp_array.append(int(line))
            counter += 1
            if counter % 2 == 0:
                self.intervals_raw_data[int(counter / 2 - 1)] = temp_array
                temp_array = []

    def create_chromosome(self, chromosome_count):
        for j in range(chromosome_count):
            temp_array = []
            for i in range(len(self.units_data_dic)):
                temp_array.append(self.units_data_dic[i+1][random.randint(
                    0, len(self.units_data_dic[i+1]) - 1)])

            self.generations[len(self.generations)] = temp_array
            temp_array = []

    def check_min(self):

        # choose a chromosome
        for j in range(len(self.generations)):
            # print(self.generations[j])
            finished = False
            while not finished:                                             # continue until the chromosome is OK
                # choose an interval to calculate the sumOfEnergies in that period
                for i in range(int(self.input_2_data[0])):
                    sumOfEnergies = 0
                    # choose the interval from each unit for e.g calculate sumOfEnergies in first interval
                    for k in range(len(self.generations[j])):
                        if self.generations[j][k][i] == 0:
                            sumOfEnergies += self.units_raw_data[k][1]
                    # print("period " , i , " is " ,  self.intervals_raw_data[i][1] , " and sumOfEnergies is ", sumOfEnergies , "\n")
                    # check if sumOfEnergies is not at least Min
                    if sumOfEnergies < self.intervals_raw_data[i][1]:
                        temp_array = []
                        # make a new chromosome and replace it
                        for i in range(len(self.units_data_dic)):
                            temp_array.append(self.units_data_dic[i+1][random.randint(
                                0, len(self.units_data_dic[i+1]) - 1)])
                        self.generations[j] = temp_array
                        temp_array = []
                        # print("chromosome changed to" , self.generations[j] , "\n")
                        break
                    if i == int(self.input_2_data[0]) - 1:
                        finished = True

    def replace_with_min(self):
        temp = []
        for i in range(len(self.fitness_data_dic)):
            arr = np.array_split(
                self.fitness_data_dic[i], self.generations_number)
            for j in range(len(arr)):
                temp.append(min(arr[j]))
            self.fitness_data_dic[i] = temp
            temp = []

    def calculate_fittness(self):
        self.fittness_list = []
        for j in range(len(self.generations)):
            minInInterval = float('inf')
            for i in range(int(self.input_2_data[0])):
                sumOfEnergies = 0
                for k in range(len(self.generations[j])):
                    if self.generations[j][k][i] == 0:
                        sumOfEnergies += self.units_raw_data[k][1]
                self.fitness_data_dic[i].append(
                    sumOfEnergies - self.intervals_raw_data[i][1])
                if sumOfEnergies < minInInterval:
                    minInInterval = sumOfEnergies
            self.fittness_list.append(minInInterval)

    def roulette_wheel_selection(self):
        self.random_list = random.choices(self.generations, weights=self.fittness_list,
                                          k=self.numberOfChromosomes)
        # for i in range(len(self.random_list)):
        #     for j in range(len(self.generations)):
        #         if self.random_list[i] == self.generations[j]:
        #             print(j)

    def crossover(self):
        temp_rand_index = []
        k = self.numberOfChromosomes * self.Pc
        temp_rand_index = random.sample(
            range(0, self.numberOfChromosomes), int(k))
        temp_length = len(temp_rand_index)
        if temp_length % 2 != 0:
            temp_length -= 1

        for i in range(0, temp_length-1, 2):
            crossover_point = random.randint(1, len(self.units_data_dic)-1)
            # print("BEFORE \n")
            # print(self.random_list[temp_rand_index[i]])
            # print(self.random_list[temp_rand_index[i+1]])
            temp_part = self.random_list[temp_rand_index[i]
                                         ][crossover_point:len(self.units_data_dic)]
            self.random_list[temp_rand_index[i]][crossover_point:len(
                self.units_data_dic)] = self.random_list[temp_rand_index[i+1]][crossover_point:len(self.units_data_dic)]
            self.random_list[temp_rand_index[i+1]][crossover_point:len(
                self.units_data_dic)] = temp_part
            # print("POINT : ", crossover_point)
            # print("AFTER \n")
            # print(self.random_list[temp_rand_index[i]])
            # print(self.random_list[temp_rand_index[i+1]])
            # print("------------------")

    def mutation(self):

        k = self.numberOfChromosomes * len(self.units_data_dic) * self.Pm
        temp_rand_index = random.sample(
            range(0, self.numberOfChromosomes * len(self.units_data_dic)), int(k))

        # print(self.random_list, "\n")
        # print(self.units_data_dic, "\n")
        # print(temp_rand_index, "\n")
        for i in range(len(temp_rand_index)):
            counter = 0
            for j in range(len(self.random_list)):
                for k in range(len(self.random_list[j])):
                    if counter == temp_rand_index[i]:
                        random_unit_index = random.randint(
                            0, len(self.units_data_dic[counter % len(self.units_data_dic)+1])-1)
                        self.random_list[j][k] = self.units_data_dic[counter % len(
                            self.units_data_dic)+1][random_unit_index]
                        # print(counter % len(self.units_data_dic)+1)
                        # print(self.units_data_dic[counter % len(self.units_data_dic)+1][random_unit_index] , "\n")

                        # print(counter, "\n",
                        #       self.random_list[j][k], "\n --------------")
                    counter += 1

    def overwrite_generation(self):
        for i in range(len(self.generations)):
            self.generations[i] = self.random_list[i]

    def plot_chart(self):
        y_axis = []
        for i in range(self.generations_number):
            y_axis.append(i+1)
        for i in range(len(self.fitness_data_dic)):
            plt.plot(y_axis, self.fitness_data_dic[i])
            plt.xlabel('x - axis')
            plt.ylabel('y - axis')
            plt.title('Season Number {}'.format(i+1))
            plt.show()