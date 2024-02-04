import random 
import math
import numpy as np
from problem import Problem


class TSP(Problem):

    # def __init__(self,population_size,offspring_size,generations,mutation_rate,iterations):
    #     print("Initializing TSP problem...")
    #     Problem.__init__(self,population_size,offspring_size,generations,mutation_rate,iterations)

    def init_population(self):
        self.population = []
        for i in range(self.population_size):
            self.population.append(self.random_chromosome())
        print(self.population[0])


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

        # Fitness is the inverse of the total distance
        fitness = 1 / total_distance

        return fitness
    
    def crossover(self,chromosome, other):
        # Perform crossover to create a new chromosome from two parents
        crossover_point = np.random.randint(1, len(chromosome) - 1)

        # Create a new chromosome by combining parts of both parents
        new_chromosome = np.concatenate((chromosome[:crossover_point], other.chromosome[crossover_point:]))

        return new_chromosome

    def mutate(self,chromosome):
        # Perform mutation by swapping two cities in the chromosome
        mutation_point1, mutation_point2 = np.random.choice(len(chromosome), 2, replace=False)

        # Create a new chromosome with the cities swapped
        new_chromosome = np.copy(chromosome)
        new_chromosome[mutation_point1], new_chromosome[mutation_point2] = (
            new_chromosome[mutation_point2],
            new_chromosome[mutation_point1]
        )

        return new_chromosome

    def random_chromosome(self):
        #generate random chromosome from TSP set
        solution = list(range(1,len(self.data)+1))
        random.shuffle(solution)
        fitness = self.calculate_fitness(solution)
        chromosome = (solution,fitness)
        return chromosome

class EA:

    def __init__(self,population_size, offsprings,generations,mutation_rate,iterations,data):
        TSP(population_size,offsprings,generations,mutation_rate,iterations,data)

    def run(self):
        pass

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

def main():
    data = ReadFile("qa194.tsp").read()
    # print(data[0])
    EA(30, 10, 50, 0.5, 10,data)
    # print(data)

main()