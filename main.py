from EA import EA

def main():
    filename = "qa194.tsp"
    pop_size = 30
    offspring_size = 10
    generations_no = 50
    mutation_rate = 0.5
    iterations = 10
    problem = "TSP"
    parent_selection = "tournament_selection_23"
    survivor_selection = "truncation"
    EA(pop_size, offspring_size, generations_no, mutation_rate, iterations, problem, parent_selection, survivor_selection, filename).run()

main()