import random
import numpy as np
from problem import Problem

class JSSP(Problem):
    def __init__(self, population_size, offspring_size, generations, mutation_rate, iterations, data):
        super().__init__(population_size, offspring_size, generations, mutation_rate, iterations, data)
        self.population = []  # Add this line to initialize the population attribute
        # Initialize the population with random individuals
        for _ in range(population_size):
            chromosome = self.random_chromosome()
            fitness = self.calculate_fitness(chromosome)
            self.population.append((chromosome, fitness))

    def calculate_fitness(self, chromosome):
        # Calculate the makespan of a chromosome
        num_jobs = len(chromosome)
        num_machines = len(chromosome[0])
        machine_end_times = np.zeros(num_machines)
        job_end_times = np.zeros(num_jobs)
        for i in range(num_jobs):
            for j in range(num_machines):
                # Calculate start time for each job on each machine
                if i == 0 and j == 0:
                    start_time = 0
                elif j == 0:
                    start_time = job_end_times[i - 1]
                elif i == 0:
                    start_time = machine_end_times[j - 1]
                else:
                    start_time = max(job_end_times[i - 1], machine_end_times[j - 1])
                # Calculate end time for each job on each machine
                end_time = start_time + chromosome[i][j]
                machine_end_times[j] = end_time
                job_end_times[i] = end_time
        return max(machine_end_times)

    def crossover(self, chromosome_tuple, other_tuple):
        # Extract chromosomes from tuples
        chromosome = np.array(chromosome_tuple[0])
        other = np.array(other_tuple[0])

        # Perform crossover to create a new chromosome from two parents
        crossover_point = np.random.randint(1, len(chromosome) - 1)

        # Flatten the arrays before concatenation
        flat_chromosome = chromosome.flatten()
        flat_other = other.flatten()

        # Create a new chromosome by combining parts of both parents
        new_chromosome = np.concatenate((flat_chromosome[:crossover_point], flat_other[crossover_point:]))
        # Convert back to 2D array
        new_chromosome = new_chromosome.reshape(chromosome.shape)

        fitness = self.calculate_fitness(new_chromosome)
        return (new_chromosome, fitness)

    def mutate(self, chromosome, mutation_rate):
        # Perform mutation by swapping two cities in the chromosome based on mutation rate
        new_chromosome = chromosome.copy()  # Copy the chromosome to avoid modifying the original
        for i in range(len(new_chromosome)):
            if np.random.random() < mutation_rate:
                mutation_point = np.random.randint(0, len(new_chromosome))
                new_chromosome[i], new_chromosome[mutation_point] = new_chromosome[mutation_point], new_chromosome[i]
        return new_chromosome

    def random_chromosome(self):
        # Generate a random chromosome from JSSP set
        solution = np.random.permutation(self.data)
        return solution
    
    def fitness_prop_selection(self, p=False, s=False):
        if not p and not s:
            print("Specify whether to use the function for parent or survivor selection")
            return 
        # Select two parents using fitness proportionate selection
        fitness_values = [x[1] for x in self.population]
        total_fitness = sum(fitness_values)
        probabilities = [x / total_fitness for x in fitness_values]
        if p:
            choice = np.random.choice(range(len(self.population)), 2, p=probabilities, replace=False)
            parents = [self.population[choice[0]], self.population[choice[1]]]
            return parents
        if s:
            choice = np.random.choice(range(len(self.population)), self.population_size, p=probabilities, replace=False)
            survivors = [self.population[x] for x in choice]
            return survivors
        
    def rank_based_selection(self, p=False, s=False):
        if not p and not s:
            print("Specify whether to use the function for parent or survivor selection")
            return 
        # Select two parents using rank-based selection
        fitness_sorted = sorted(self.population, key=lambda x: x[1])
        fitness_range = range(1, len(fitness_sorted) + 1)
        probabilities = [x / sum([y for y in fitness_range]) for x in reversed(fitness_range)]
        if p:
            choice = np.random.choice(range(len(self.population)), 2, p=probabilities, replace=False)
            parents = [self.population[choice[0]], self.population[choice[1]]]
            return parents
        if s:
            choice = np.random.choice(range(len(self.population)), self.population_size, p=probabilities, replace=False)
            survivors = [self.population[x] for x in choice]
            return survivors
        
    def tournament_selection(self, p=False, s=False, n=2):
        self.tournament_size = n
        if not p and not s:
            print("Specify whether to use the function for parent or survivor selection")
            return
        if p:
            parents = [self.population[index] for index in np.random.choice(range(len(self.population)), 2, replace=False)]
            return parents
        if s:
            survivors = [self.population[index] for index in np.random.choice(range(len(self.population)), self.tournament_size, replace=False)]
            return survivors
        
    def truncation(self, p=False, s=False):
        if not p and not s:
            print("Specify whether to use the function for parent or survivor selection")
            return 
        if p:
            # Selects two parents using truncation selection
            parents = sorted(self.population, key=lambda x: x[1])[:2]
            return parents
        if s:
            # Selects survivors using truncation selection
            survivors = sorted(self.population, key=lambda x: x[1])[:self.population_size]
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
        
    def survivor_selection(self):
        # Select survivors using truncation selection
        return sorted(self.population, key=lambda x: x[1])[:self.population_size]
    
class EA: 
    def __init__(self, population_size, offspring_size, generations, mutation_rate, iterations, problem_name, parent_selection_scheme, survivor_selection_scheme, data):
        self.problem_name = globals()[problem_name]
        self.parent_selection_scheme = parent_selection_scheme
        self.survivor_selection_scheme = survivor_selection_scheme
        self.instance = self.problem_name(population_size, offspring_size, generations, mutation_rate, iterations, data)

    def run(self):
        top_solutions = []
        parent_selection_function = getattr(self.instance, self.parent_selection_scheme)
        survivor_selection_function = getattr(self.instance, self.survivor_selection_scheme)
        if not callable(parent_selection_function) or not callable(survivor_selection_function):
            print("Invalid selection scheme")
            return
        
        for i in range(self.instance.iterations):
            for j in range(self.instance.generations):
                for k in range(self.instance.offspring_size):
                    parents = parent_selection_function(p=True)
                    offspring = self.instance.crossover(parents[0], parents[1])
                    self.instance.population.append(offspring)
                survivors = survivor_selection_function(s=True)
                self.instance.population = survivors
            top_solutions.append(min(self.instance.population, key=lambda x: x[1]))
        x = [x[1] for x in top_solutions]
        print("Top solutions: ", x)

class ReadFile:
    def __init__(self, filename):
        self.filename = filename
        self.data = self.read_file()
        
    def read_file(self):
        with open(self.filename, 'r') as file:
            data = file.readlines()
            data = [x.strip() for x in data]
            data = [x.split() for x in data]
            data = [[int(y) for y in x] for x in data]
        return data

def main():
    data = ReadFile("abz5").read_file()
    pop_size = 500
    offspring_size = 25
    generations_no = 200
    mutation_rate = 0.5
    iterations = 10
    problem = "JSSP"
    parent_selection = "random"
    survivor_selection = "truncation"
    EA(pop_size, offspring_size, generations_no, mutation_rate, iterations, problem, parent_selection, survivor_selection, data).run()

main()