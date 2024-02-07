import numpy as np
from problem import Problem

class JSSP(Problem):

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
        fitness = self.calculate_fitness(solution)
        chromosome = (solution, fitness)
        return chromosome
    
    def read_file(self):
        with open(self.filename, 'r') as file:
            data = file.readlines()
            data = [x.strip() for x in data]
            data = [x.split() for x in data]
            data = [[int(y) for y in x] for x in data]
        return data