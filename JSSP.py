import random
import numpy as np
from problem import Problem

class JSSP(Problem):

    # def calculate_fitness(self, chromosome, machine_data):
    #     # Calculate the makespan of a chromosome
    #     num_jobs, num_machines, job_data = self.read_file()
    #     print("printing data", chromosome)
    #     print("printing machine",machine_data)
    #     job_end_times = [0] * num_jobs
        
    #     # Ensure that chromosome has the correct dimensions
    #     if len(chromosome) != num_jobs:
    #         raise ValueError("Chromosome length does not match the number of jobs")
        
    #     for i in range(num_jobs):
    #         # Ensure that each job in the chromosome has the correct number of machines
    #         if len(chromosome[i]) != num_machines:
    #             raise ValueError(f"Chromosome does not have the expected number of machines for job {i}")
            
    #         for j in range(num_machines):
    #             # Ensure that each machine for a job has the expected structure
    #             if len(chromosome[i][j]) != 2:
    #                 raise ValueError(f"Invalid machine structure in chromosome for job {i}, machine {j}")
                
    #             # Calculate start time for each job on each machine
    #             if i == 0 and j == 0:
    #                 start_time = 0
    #             elif j == 0:
    #                 start_time = job_end_times[i - 1]
    #             elif i == 0:
    #                 start_time = job_end_times[i]
    #             else:
    #                 start_time = max(job_end_times[i - 1], job_end_times[i])
                
    #             # Calculate end time for each job on each machine
    #             end_time = start_time + chromosome[i][j][1]
    #             job_end_times[i] = end_time
        
    #     return max(job_end_times)

    # def calculate_fitness(self, chromosome):

    #     num_jobs, num_machines, job_data = self.read_file()
    #     print("printing data", chromosome)
    #     machine_data = dict()
    #     for i in range(len(chromosome[0])):
    #         for idx,j in enumerate(chromosome):
    #             if j[i][0] in machine_data:
    #                 machine_data[j[i][0]].append((idx,j[i][1]))
    #             else:
    #                 machine_data[j[i][0]] = [(idx,j[i][1])]

    #     print("printing machine",machine_data)
    #     job_end_times = [0] * num_jobs
    #     for job in chromosome:
            

    def make_unique(self, chromosome):
        # Ensure uniqueness of jobs in the chromosome
        seen = set()
        unique_chromosome = []
        for job in chromosome:
            job_tuple = tuple(job)  # Convert the list to a tuple
            if job_tuple not in seen:
                unique_chromosome.append(job)
                seen.add(job_tuple)
        return unique_chromosome
    
    def crossover(self, parent1, parent2):
        # Perform crossover to create a new chromosome from two parents
        num_jobs = len(parent1[0])
        crossover_point = np.random.randint(1, num_jobs)

        # Create a new chromosome by combining parts of both parents
        new_chromosome1 = parent1[0][:crossover_point] + parent2[0][crossover_point:]
        new_chromosome2 = parent2[0][:crossover_point] + parent1[0][crossover_point:]

        # Ensure uniqueness of jobs in each chromosome
        new_chromosome1 = self.make_unique(new_chromosome1)
        new_chromosome2 = self.make_unique(new_chromosome2)
        
        # Check the shape of the new chromosomes
        print("Shape of new chromosome 1:", len(new_chromosome1))
        print("Shape of new chromosome 2:", len(new_chromosome2))

        fitness1 = self.calculate_fitness(new_chromosome1)
        fitness2 = self.calculate_fitness(new_chromosome2)
        offsprings = [(new_chromosome1, fitness1), (new_chromosome2, fitness2)]
        # print(offsprings[0][0])
        return offsprings

    def mutate(self, chromosome):
        # Perform mutation by swapping two jobs in the chromosome based on mutation rate
        jobs = chromosome[0].copy()  # Extract the jobs from the chromosome tuple
        num_jobs = len(jobs)

        if np.random.random() < self.mutation_rate:
            # Randomly select two different jobs to swap
            job_index1, job_index2 = np.random.choice(num_jobs, 2, replace=False)
            # Swap the jobs
            jobs[job_index1], jobs[job_index2] = jobs[job_index2], jobs[job_index1]

        # Ensure uniqueness of jobs in the chromosome
        jobs = self.make_unique(jobs)

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
        # print(chromosome[0])
        return chromosome

    def read_file(self):
        with open(self.filename, 'r') as file:
            lines = file.readlines()
            num_jobs, num_machines = map(int, lines[0].split())
            data = lines[1:]
            data = [x.strip() for x in data]
            data = [x.split() for x in data]
            job_data = [[int(y) for y in x] for x in data]

        return num_jobs, num_machines, job_data