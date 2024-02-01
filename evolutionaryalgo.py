import random 

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

class EA:
    def __init__(self,chromosome_length,population_size):
        self.chromosome_length = chromosome_length
        self.population_size = population_size
        self.population = self.init_population()

    def init_population(self):
        pass

    def selection(self):
        pass

    def crossover(self):
        pass

    def mutation(self):
        pass

    def run(self):
        pass

print("Hello World Azeem!")