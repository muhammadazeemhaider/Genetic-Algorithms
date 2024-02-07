import random 
import math
import numpy as np
from problem import Problem

class TSP(Problem):

    def calculate_fitness(self,chromosome):
        total_distance = 0.0
        num_cities = len(chromosome)

        for i in range(num_cities - 1):
            # Calculate Euclidean distance between consecutive cities
            city1 = self.data[chromosome[i] - 1]
            city2 = self.data[chromosome[i + 1] - 1]
            distance = math.sqrt((city2[0] - city1[0])**2 + (city2[1] - city1[1])**2)
            total_distance += distance

        # Add distance from the last city back to the starting city
        total_distance += math.sqrt((self.data[-1][0] - self.data[0][0])**2 + 
                                    (self.data[-1][1] - self.data[0][1])**2)

        return total_distance
    
    def crossover(self,chromosome, other):
        # Perform crossover to create a new chromosome from two parents
        crossover_point = np.random.randint(1, len(chromosome[0]) - 1)

        # Create a new chromosome by combining parts of both parents
        new_chromosome1 = list(np.concatenate((chromosome[0][:crossover_point], other[0][crossover_point:])))
        new_chromosome2 = list(np.concatenate((other[0][:crossover_point], chromosome[0][crossover_point:])))
        fitness1 = self.calculate_fitness(new_chromosome1)
        fitness2 = self.calculate_fitness(new_chromosome2)
        offsprings = [(new_chromosome1,fitness1),(new_chromosome2,fitness2)]
        return offsprings

    def mutate(self, chromosome, mutation_rate):
        # Perform mutation by swapping two cities in the chromosome based on mutation rate
        new_chromosome = chromosome.copy()  # Copy the chromosome to avoid modifying the original
        for i in range(len(new_chromosome)):
            if np.random.random() < mutation_rate:
                mutation_point = np.random.randint(0, len(new_chromosome))
                new_chromosome[i], new_chromosome[mutation_point] = new_chromosome[mutation_point], new_chromosome[i]
        return new_chromosome

    def random_chromosome(self):
        #generate random chromosome from TSP set
        solution = list(range(1,len(self.data)+1))
        random.shuffle(solution)
        fitness = self.calculate_fitness(solution)
        chromosome = (solution,fitness)
        return chromosome
    
    def read_file(self):
        data = ReadFile(self.filename).read()
        return data


#Class for reading file
class ReadFile:
    def __init__(self,filename):
        self.filename = filename
        self.data = []

    # open file
    def read(self):
        try:
            with open(self.filename) as f:
                content = f.readlines()
                print("Reading file {}...".format(self.filename))
                self.parse_data(content)
                print("File read successfully")
                return self.data
        except:
            print("Error: File {} not found".format(self.filename))

    # reads and parses city data
    def parse_data(self,content):
        nodes_start = False

        for line in content:
            if line.startswith("NODE_COORD_SECTION"):
                nodes_start = True
                continue
            
            if nodes_start:
                if line.startswith("EOF"):
                    break
                self.data.append(self.parse_city_data(line))

        return self.data

    #formats city data
    def parse_city_data(self,city_data):
        city = city_data.split()
        city = (float(city[1]),float(city[2]))
        return city