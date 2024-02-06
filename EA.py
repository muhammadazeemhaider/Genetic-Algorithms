from JSSP import JSSP
from TSP import TSP

class EA: 
    def __init__(self, population_size, offspring_size, generations, mutation_rate, iterations, problem_name, parent_selection_scheme, survivor_selection_scheme, filename):
        self.problem_name = globals()[problem_name]
        self.parent_selection_scheme = parent_selection_scheme
        self.survivor_selection_scheme = survivor_selection_scheme
        self.instance = self.problem_name(population_size, offspring_size, generations, mutation_rate, iterations, filename)

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
                for k in range(self.instance.offspring_size):
                    parents = parent_selection_function(p=True)
                    offspring = self.instance.crossover(parents[0], parents[1])
                    self.instance.population.append(offspring)
                survivors = survivor_selection_function(s=True)
                self.instance.population = survivors
            top_solutions.append(min(self.instance.population, key=lambda x: x[1]))
        x = [x[1] for x in top_solutions]
        print("Top solutions: ", x)