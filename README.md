# Genetic Algorithms

This project contains evolutionary algorithms written in Python as an assignment for the course CS-451: Computational Intelligence at Habib University taught by Dr.Saleha Raza. Chromosome representation and results of each problem are present inside the report titled __Assignment01.pdf__ The evolutionary algorithms are implemented to find optimal solutions for combinatorial problems described below:

## Dependencies
* Python
* Numpy
* Matplotlib
* Pandas

## Problem Introduction
### Travelling Salesman Problem

Travelling Salesman Problem([TSP](https://en.wikipedia.org/wiki/Travelling_salesman_problem)) is a widely popular n combinatorial problem that gets more complex to solve through greedy algorithms as we increase the number of cities. It involves finding the shortest path that visits every city only once.

### Job Shop Scheduling Problem 
Job Shop Scheduling Problem ([JSSP](https://en.wikipedia.org/wiki/Job-shop_scheduling)) is also another famous n combinatorial problem. It involves running different operations of a job on their required machines. The optimization constraint is to use the machines in such a way that the time is minimized.

### Polygona Lisa
The brilliantly named problem is not so widely known like the above problem statements. It involves replicating the original image of [Mona Lisa](https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Mona_Lisa%2C_by_Leonardo_da_Vinci%2C_from_C2RMF_retouched.jpg/405px-Mona_Lisa%2C_by_Leonardo_da_Vinci%2C_from_C2RMF_retouched.jpg) using 50 triangles.

## Algorithm

The algorithm follows the following steps:
* Generating a random population of _population_size_ and assign them their fitness values.
* Select parents using a _parent_selection_scheme_. 
* Generate 2 offsprings from 2 parents using crossover method.
* Mutate these offsprings according to the _mutation_rate_ probability.
* Caculate fitness of new offsprings.
* Select members to be part of the next generation through _survivor_selection_scheme_
* Repeat the steps until the end of _generations_no_

The _italicized_ words in the above algorithm are configurable by the user during runtime.

## Usage

```python
python .\main.py p1 p2 .. p9
```

For a complete list of parameters and their values refer [below](#parameters).

### Example

```python
python .\main.py TSP qa194.tsp ts_4 tr 30 10 50 0.5 10
```

## Parameters

The following is the list of all parameters from p1-p9 to be supplied to run the code:

1. **Problem Name**: Provide the name of the problem you want to run. In our project there are only three available which are: TSP, JSSP, MonaLisa.
2. **File Name**: Provide the input file name from which the data will be read. For mona lisa provide the original image.
3. **Parent Selection Scheme**: Specify a [selection scheme](#selection-schemes) to be used for choosing parents to generate offsprings.
4. **Survival Selection Scheme**: Specify a [selection scheme](#selection-schemes) to decide which chromosomes will die out in the current generation.
5. **Population Size**: Initial population size.
6. **Offspring Size**: Number of offsprings to be generated in each generation.
7. **Generations Number**: Number of generations the algorithm will run. This is also the termination criteria for our algorithm.
8. **Mutation Rate**: The probability that each offspring will go through the mutation process.
9. **Iterations**: Number of iterations of the whole process to generate multiple samples for averaging.

## Selection Schemes

The following selection schemes have been implemented with the following abbrevation to provide to call them.

* **Random**: rn
* **Tournament**: ts_*size*, size specifies the size of the tournament
* **Rank Based Selection**: rbs
* **Fitness Proportion Selection**: fps
* **Truncation**: tr

## Authors

* [Azeem Haider](https://github.com/A-Haider13)
* [Mustafa Sohail](https://github.com/Mustafasohail7)

## License

[MIT](https://choosealicense.com/licenses/mit/)
