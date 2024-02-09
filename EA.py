from JSSP import JSSP
from TSP import TSP
import matplotlib.pyplot as plt

class EA: 
    def __init__(self, population_size, offspring_size, generations, mutation_rate, iterations, problem_name, parent_selection_scheme, survivor_selection_scheme, filename):
        self.problem_name = globals()[problem_name]
        self.parent_selection_scheme = parent_selection_scheme
        self.survivor_selection_scheme = survivor_selection_scheme
        self.instance = self.problem_name(population_size, offspring_size, generations, mutation_rate, iterations, filename)
        self.iterations = iterations  # Store the number of iterations

    def run(self):
        top_solutions = []

        if "tournament_selection" in self.parent_selection_scheme:
            psf = self.parent_selection_scheme[:20]
            tn_size = self.parent_selection_scheme.split("_")[-1]
            self.instance.tournament_size = int(tn_size)
            self.parent_selection_scheme = psf

        if "tournament_selection" in self.survivor_selection_scheme:
            ssf = self.survivor_selection_scheme[:20]
            tn_size = self.survivor_selection_scheme.split("_")[-1]
            self.instance.tournament_size = int(tn_size)
            self.survivor_selection_scheme = ssf

        parent_selection_function = getattr(self.instance, self.parent_selection_scheme)
        survivor_selection_function = getattr(self.instance, self.survivor_selection_scheme)
        if not callable(parent_selection_function) or not callable(survivor_selection_function):
            print("Invalid selection scheme")
            return
        
        for i in range(self.instance.iterations):
            for j in range(self.instance.generations):
                for k in range(0,self.instance.offspring_size,2):
                    parents = parent_selection_function(p=True)
                    offsprings = self.instance.crossover(parents[0], parents[1])
                    self.instance.population.append(self.instance.mutate(offsprings[0]))
                    self.instance.population.append(self.instance.mutate(offsprings[1]))
                    self.instance.population.append(offsprings[0])
                    self.instance.population.append(offsprings[1])
                survivors = survivor_selection_function(s=True)
                self.instance.population = survivors
                print("Generation: ", j+1)
                print("Top solution for this iteration: ", min(self.instance.population, key=lambda x: x[1])[1])
            top_solutions.append(min(self.instance.population, key=lambda x: x[1]))
            self.instance.init_population()
        
        # Plot the line graph
        x = list(range(1, self.iterations + 1))  # x-axis values
        y = [solution[1] for solution in top_solutions]  # y-axis values
        plt.plot(x, y)
        plt.xlabel('Iteration')
        plt.ylabel('Fitness')
        plt.title('Fitness over Iterations')
        plt.show()