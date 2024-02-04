class Problem():
    def __init__(self,population_size,offspring_size,generations,mutation_rate,iterations,data):
        self.population_size = population_size
        self.offspring_size = offspring_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.iterations = iterations
        self.data = data
        self.init_population()

    def init_population(self):
        pass

    def calculate_fitness(self,chromosome):
        pass
    
    def select_parents(self):
        pass

    def crossover(self,chromosome1,chromosome2):
        pass

    def mutation(self,chromosome):
        pass
