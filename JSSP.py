import random
import numpy as np
from problem import Problem

class JSSP(Problem):

    def calculate_fitness(self, chromosome):
        # Calculate the makespan for a given chromosome
        print("Calculating fitness for chromosome:", chromosome)
        occurences = dict()
        end_times = dict()
        end_times_machine = dict()
        for job in chromosome:
            # print("ending_times",end_times)
            if job in occurences:
                occurences[job] += 1
            else:
                occurences[job] = 0
            occurence = occurences[job]
            machine = self.job_machine[job][occurence]
            time = self.job_time[job][occurence]

            if occurence == 0:
                start_time = 0
            else:
                start_time = end_times[job][occurence-1]

            if machine in end_times_machine:
                start_time = max(start_time, end_times_machine[machine])
            else:
                start_time = start_time

            end_time = start_time + time
            if job in end_times:
                end_times[job].append(end_time)
            else:
                end_times[job] = [end_time]

            if machine in end_times_machine:
                end_times_machine[machine] = max(end_times_machine[machine], end_time)
            else:
                end_times_machine[machine] = end_time

        makespan = max(end_times_machine.values())
        
        return makespan
    


    
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
        chromosome = []
        for i in range(self.num_jobs):
            for j in range(self.num_operations):
                chromosome.append(i)
        random.shuffle(chromosome)
        fitness = self.calculate_fitness(chromosome)
        return (chromosome, fitness)

    def read_file(self):
        with open(self.filename, 'r') as file:
            lines = file.readlines()
            self.num_jobs, self.num_machines = map(int, lines[0].split())
            data = lines[1:]
            data = [x.strip() for x in data]
            data = [x.split() for x in data]
            job_data = [[int(y) for y in x] for x in data]
            self.job_machine = dict()
            self.job_time = dict()
            for idx,i in enumerate(job_data):
                self.job_machine[idx] = [i[j] for j in range(0,len(i),2)]
                self.job_time[idx] = [i[j] for j in range(1,len(i),2)]
            self.num_operations = int(len(job_data[0])/2)

        return job_data