import random 
import math
import numpy as np
from Problem import Problem


class TSP(Problem):

    def init_population(self):
        self.population = []
        for i in range(self.population_size):
            self.population.append(self.random_chromosome())


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
        new_chromosome = list(np.concatenate((chromosome[0][:crossover_point], other[0][crossover_point:])))
        fitness = self.calculate_fitness(new_chromosome)
        return (new_chromosome, fitness)

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
    
    def fitness_prop_selection(self,p=False,s=False):
        if not p and not s:
            print("Specify whether to use function for parent or survivor selection")
            return 
        #selects two parents using fitness proportionate selection
        fitness_values = [x[1] for x in self.population]
        total_fitness = sum(fitness_values)
        probabilities = [x/total_fitness for x in fitness_values]
        if p:
            choice = np.random.choice(range(len(self.population)), 2, p=probabilities, replace=False)
            parents = [self.population[choice[0]], self.population[choice[1]]]
            return parents
        if s:
            choice = np.random.choice(range(len(self.population)), self.population_size, p=probabilities, replace=False)
            survivors = [self.population[x] for x in choice]
            return survivors
    
    def rank_based_selection(self,p=False,s=False):
        if not p and not s:
            print("Specify whether to use function for parent or survivor selection")
            return 
        #selects two parents using rank based selection
        fitness_sorted = sorted(self.population, key=lambda x: x[1])
        # print(fitness_sorted)
        fitness_range = range(1,len(fitness_sorted)+1)
        probabilities = [x/sum([y for y in fitness_range]) for x in reversed(fitness_range)]
        # print(probabilities)
        if p:
            choice = np.random.choice(range(len(self.population)), 2, p=probabilities, replace=False)
            parents = [fitness_sorted[choice[0]], fitness_sorted[choice[1]]]
            return parents
        if s:
            choice = np.random.choice(range(len(self.population)), self.population_size, p=probabilities, replace=False)
            survivors = [fitness_sorted[x] for x in choice]
            return survivors

    def tournament_selection(self,p=False,s=False,n=2):
        self.tournament_size=n
        if not p and not s:
            print("Specify whether to use function for parent or survivor selection")
            return 
        #selects two parents using tournament selection
        if p:
            parents = [self.tournament(), self.tournament()]
            return parents
        if s:
            survivors = [self.tournament() for i in range(self.population_size)]
            return survivors
        
    def tournament(self):
        rand_n = []
        for i in range(self.tournament_size):
            rand_n.append(random.randint(1,len(self.population)))
        players = [self.population[i-1] for i in rand_n]
        ranking = sorted(players, key=lambda x: x[1])
        return ranking[0]

    def truncation(self,p=False,s=False):
        if not p and not s:
            print("Specify whether to use function for parent or survivor selection")
            return 
        
        fitness_sorted = sorted(self.population, key=lambda x: x[1])
        if p:
            parents = [fitness_sorted[0],fitness_sorted[1]]
            return parents
        if s:
            survivors = [fitness_sorted[i] for i in range(self.population_size)]
            return survivors
            
    def random(self,p=False,s=False):
        if not p and not s:
            print("Specify whether to use function for parent or survivor selection")
            return 
        
        if p:
            choice = [random.randint(1,self.population_size)-1 for i in range(2)]
            parents = [self.population[choice[0]],self.population[choice[1]]]
            return parents
        if s:
            choice = [random.randint(1,self.population_size)-1 for i in range(self.population_size)]
            survivors = [self.population[choice[i]] for i in choice]
            return survivors



class EA:

    def __init__(self,population_size,offsprings,generations,mutation_rate,iterations,problem_name,parent_selection_scheme,survivor_selection_scheme,data):

        self.parent_selection_scheme = parent_selection_scheme
        self.survivor_selection_scheme = survivor_selection_scheme
        
        #calling the problem class
        self.problem_name = globals()[problem_name]
        self.instance = self.problem_name(population_size,offsprings,generations,mutation_rate,iterations,data)

    def run(self):

        top_solutions = []

        #selecting the parent and survivor selection schemes
        parent_selection_function = getattr(self.instance, self.parent_selection_scheme)
        survivor_selection_function = getattr(self.instance, self.survivor_selection_scheme)
        #returns error if the user has selected invalid selection schemes
        if not callable(parent_selection_function) or not callable(survivor_selection_function):
            print("Invalid selection scheme")
            return
        
        #running the EA
        for i in range(self.instance.iterations):
            for j in range(self.instance.generations):
                for k in range(self.instance.offspring_size):
                    parents = parent_selection_function(p=True)
                    offspring = self.instance.crossover(parents[0],parents[1])
                    self.instance.population.append(offspring)
                    # break
                # break
                survivors = survivor_selection_function(s=True)
                self.instance.population = survivors
            top_solutions.append(min(self.instance.population, key=lambda x: x[1]))
            # break
        x = [x[1] for x in top_solutions]
        print("Top solutions: ", x)


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
    pop_size = 30
    offspring_size = 10
    generations_no = 50
    mutation_rate = 0.5
    iterations = 10
    problem = "TSP"
    parent_selection = "random"
    survivor_selection = "truncation"
    EA(pop_size,offspring_size,generations_no,mutation_rate,iterations,problem,parent_selection,survivor_selection,data).run()


main()