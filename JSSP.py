import random
import numpy as np
from problem import Problem

class JSSP(Problem):

    def calculate_fitness(self, chromosome):
        # Calculate the makespan for a given chromosome
        # print("Calculating fitness for chromosome:", chromosome)
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
        crossover_point = np.random.randint(1,len(parent1[0])//2)
        crossover_point_2 = np.random.randint(len(parent1[0])//2,len(parent1[0])-1)

        first_half = parent1[0][:crossover_point] 
        second_half = parent2[0][crossover_point:crossover_point_2]
        third_half = parent1[0][crossover_point_2:]
        
        offspring1 = self.make_unique(first_half, second_half, third_half)

        first_half = parent2[0][:crossover_point]
        second_half = parent1[0][crossover_point:crossover_point_2]
        third_half = parent2[0][crossover_point_2:]

        offspring2 = self.make_unique(first_half, second_half,third_half)

        fitness1 = self.calculate_fitness(offspring1)
        fitness2 = self.calculate_fitness(offspring2)

        offsprings = [(offspring1,fitness1),(offspring2,fitness2)]
        return offsprings

    def make_unique(self, first_half, second_half, third_half):
        occurences = dict()
        offspring  = first_half.copy()
        for i in first_half:
            if i in occurences:
                occurences[i] += 1
            else:
                occurences[i] = 1
        
        for i in second_half:
            if i in occurences:
                if occurences[i]<self.num_operations:
                    occurences[i] += 1
                    offspring.append(i)
            else:
                occurences[i] = 1
                offspring.append(i)

        for i in third_half:
            if i in occurences:
                if occurences[i]<self.num_operations:
                    occurences[i] += 1
                    offspring.append(i)
            else:
                occurences[i] = 1
                offspring.append(i)

        for i in occurences:
            if occurences[i]<self.num_operations:
                for j in range(self.num_operations-occurences[i]):
                    offspring.append(i)

        return offspring
        
    def mutate(self, chromosome, swaps=1):
        # Perform mutation by swapping two jobs in the chromosome based on mutation rate
        jobs = chromosome[0].copy()  # Extract the jobs from the chromosome tuple
        fitness = chromosome[1]

        if np.random.random() < self.mutation_rate:
            for i in range(swaps):
                idx = np.random.randint(0, len(jobs), 2)
                while idx[0] == idx[1]:
                    idx = np.random.randint(0, len(jobs), 2)
                
                while jobs[idx[1]]==jobs[idx[0]]:
                    idx[1]+=1
                    idx[1]=idx[1]%len(jobs)

                jobs[idx[0]], jobs[idx[1]] = jobs[idx[1]], jobs[idx[0]]
            fitness = self.calculate_fitness(jobs)
        
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