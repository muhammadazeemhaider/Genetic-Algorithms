import random
from problem import Problem

class JSSP(Problem):

    def calculate_fitness(self, chromosome):
        # Calculate the makespan of a chromosome
        num_jobs = len(chromosome)
        num_machines = len(chromosome[0])
        machine_end_times = [0] * num_machines
        job_end_times = [0] * num_jobs
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
        chromosome = chromosome_tuple[0]
        other = other_tuple[0]

        # Perform crossover to create a new chromosome from two parents
        crossover_point = random.randint(1, len(chromosome) - 1)

        # Flatten the arrays before concatenation
        flat_chromosome = [item for sublist in chromosome for item in sublist]
        flat_other = [item for sublist in other for item in sublist]

        # Create a new chromosome by combining parts of both parents
        new_chromosome = flat_chromosome[:crossover_point] + flat_other[crossover_point:]
        # Convert back to 2D array
        new_chromosome = [new_chromosome[i:i+len(chromosome[0])] for i in range(0, len(new_chromosome), len(chromosome[0]))]

        fitness = self.calculate_fitness(new_chromosome)
        return (new_chromosome, fitness)

    def mutate(self, chromosome, mutation_rate):
        # Perform mutation by swapping two cities in the chromosome based on mutation rate
        new_chromosome = [list(job) for job in chromosome]  # Copy the chromosome to avoid modifying the original
        for i in range(len(new_chromosome)):
            if random.random() < mutation_rate:
                mutation_point = random.randint(0, len(new_chromosome))
                new_chromosome[i], new_chromosome[mutation_point] = new_chromosome[mutation_point], new_chromosome[i]
        return new_chromosome

    def random_chromosome(self):
        jobs = []
        for job_data in self.data:
            job = []
            for i in range(0, len(job_data), 2):  # Iterate over pairs of elements in the job data
                machine_number = job_data[i]
                processing_time = job_data[i + 1]
                job.append((machine_number, processing_time))
            jobs.append(job)

        # //TODO: Implement random_chromosome
        random.shuffle(jobs)

        # //TODO: un-linearize the chromosome
        solution = [pair for job in jobs for pair in job]

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