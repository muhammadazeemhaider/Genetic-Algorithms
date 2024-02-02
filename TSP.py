import random 
import Problem

class Chromosome:
    def __init__(self,chromosome):
        self.chromosome = chromosome
        self.fitness = self.calculate_fitness()

    def calculate_fitness(self):
        pass

    def crossover(self,other):
        pass

    def mutate(self):
        pass

class TSP(Problem):
    # def __init__(self,population_size,offspring_size,generations,mutation_rate,iterations):
    #     Problem.__init__(self,population_size,offspring_size,generations,mutation_rate,iterations)

    def init_population(self):
        self.population = []
        for i in range(self.population_size):
            self.population.append(self.random_chromosome())

    def fitness(self,chromosome):
        pass

    def crossover(self,chromosome1,chromosome2):
        pass

    def mutation(self,chromosome):
        pass

    def random_chromosome(self):
        #generate random chromosome from TSP set
        pass

class EA:

    def __init__(self,population_size, offsprings,generations,mutation_rate,iterations):
        self.population_size = population_size
        self.offsprings = offsprings
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.iterations = iterations
        self.population = self.init_population()

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
        city = (int(city[0]),float(city[1]),float(city[2]))
        return city

def main():
    data = ReadFile("qa194.tsp").read()
    EA(30, 10, 50, 0.5, 10)
    print(data)

main()