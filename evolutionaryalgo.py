import random

def main():
    print("Hello World!")

# initialize population for evolutionary algorithm randomly or with a heuristic
# size: size of the population
# selection_size: size of the selection pool
def initialize_population(size, selection_size):
    random.seed(1)
    population = []

    for i in range(selection_size):
        population.append(random.randint(0, 1))
