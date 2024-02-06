import sys
from EA import EA

def main():
    filename = sys.argv[2]
    pop_size = 30
    offspring_size = 10
    generations_no = 50
    mutation_rate = 0.5
    iterations = 10
    problem = sys.argv[1]
    parent_selection = sys.argv[3]
    survivor_selection = sys.argv[4]
    EA(pop_size, offspring_size, generations_no, mutation_rate, iterations, problem, parent_selection, survivor_selection, filename).run()

main()