import random
import numpy as np
from problem import Problem

class JSSP(Problem):

    def calculate_fitness(self, chromosome):
        # Calculate the makespan of a chromosome
        num_jobs, num_machines, job_data = self.read_file()
        # print("print num_jobs",num_jobs)
        # print("print num_machines",num_machines)
        job_end_times = [0] * num_jobs
        for i in range(num_jobs):
            for j in range(num_machines):
                # Calculate start time for each job on each machine
                if i == 0 and j == 0:
                    start_time = 0
                elif j == 0:
                    start_time = job_end_times[i - 1]
                elif i == 0:
                    start_time = job_end_times[i]
                else:
                    start_time = max(job_end_times[i - 1], job_end_times[i])
                # Calculate end time for each job on each machine
                # print("printing the error value", chromosome[i][j][1])
                end_time = start_time + chromosome[i][j][1]
                job_end_times[i] = end_time
        return max(job_end_times)

    
    def crossover(self,parent1, parent2):
        # Perform crossover to create a new chromosome from two parents
        crossover_point = np.random.randint(1, len(parent1[0]) - 1)

        # Create a new chromosome by combining parts of both parents
        first_half = parent1[0][:crossover_point]
        second_half = parent2[0][crossover_point:]
        new_chromosome1 = first_half + [x for x in second_half if x not in first_half]
        self.insert_missing(parent1,new_chromosome1)

        first_half = parent2[0][:crossover_point]
        second_half = parent1[0][crossover_point:]
        new_chromosome2 = first_half + [x for x in second_half if x not in first_half]
        self.insert_missing(parent2,new_chromosome2)

        fitness1 = self.calculate_fitness(new_chromosome1)
        fitness2 = self.calculate_fitness(new_chromosome2)
        offsprings = [(new_chromosome1,fitness1),(new_chromosome2,fitness2)]
        return offsprings

    def mutate(self, chromosome):
        # Perform mutation by swapping two jobs in the chromosome based on mutation rate
        jobs = chromosome[0].copy()  # Extract the jobs from the chromosome tuple

        r = np.random.random() < self.mutation_rate
        if r < self.mutation_rate:
            job_index = np.random.randint(0, len(jobs))
            job_swap_index = np.random.randint(0, len(jobs))
            jobs[job_index], jobs[job_swap_index] = jobs[job_swap_index], jobs[job_index]

        # Recalculate fitness for the mutated chromosome
        fitness = self.calculate_fitness(jobs)
        
        # Return the mutated chromosome as a tuple containing the jobs and their fitness
        return (jobs, fitness)

    def random_chromosome(self):
        jobs = []
        # print("printing data", self.data[2])
        for job_data in self.data[2]:
            job = []
            machines_and_times = list(zip(job_data[::2], job_data[1::2]))  # Create pairs of machine and time
            random.shuffle(machines_and_times)  # Shuffle pairs of machine and time
            for machine, processing_time in machines_and_times:
                job.append((machine, processing_time))
            jobs.append(job)

        fitness = self.calculate_fitness(jobs)

        chromosome = (jobs, fitness)
        print(chromosome[0])
        return chromosome
    
    def insert_missing(self,chromosome,new_chromosome):
        missing = []
        for i in range(1,len(chromosome[0])+1):
            if i not in new_chromosome:
                new_chromosome.append(i)
                missing.append(i)
        np.random.shuffle(missing)

    def read_file(self):
        with open(self.filename, 'r') as file:
            lines = file.readlines()
            num_jobs, num_machines = map(int, lines[0].split())
            data = lines[1:]
            data = [x.strip() for x in data]
            data = [x.split() for x in data]
            data = [[int(y) for y in x] for x in data]
        return num_jobs, num_machines, data
