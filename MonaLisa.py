import random
from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from problem import Problem
import os
import io

class MonaLisa(Problem):

    def __init__(self, population_size, offspring_size, generations, mutation_rate, iterations, filename):
        self.original_image = Image.open(filename).convert('RGBA')
        self.canvas_size = self.original_image.size
        super().__init__(population_size, offspring_size, generations, mutation_rate, iterations, filename)

    def calculate_fitness(self, polygons):
        # Calculate the fitness of a chromosome for the Mona Lisa problem
        img = Image.open("gen_mona.png")

        # Convert the images to numpy arrays
        original_array = np.array(self.original_image)
        fitness_array = np.array(img)

        # print("Original array shape:", original_array.shape)
        # print("Fitness array shape:", fitness_array.shape)

        # Calculate the fitness as the difference between the original and generated images
        fitness = np.sum((original_array - fitness_array) ** 2)
        # print("printing fitness",fitness)
        return fitness

    def crossover(self, parent1, parent2):
        # Perform crossover to create a new chromosome from two parents
        crossover_point = random.randint(1, len(parent1))

        # Create a new chromosome by combining parts of both parents
        child1 = parent1[0][:crossover_point] + parent2[0][crossover_point:]
        child2 = parent2[0][:crossover_point] + parent1[0][crossover_point:]

        fitness1 = self.calculate_fitness(child1)
        fitness2 = self.calculate_fitness(child2)

        offsprings = [(child1, fitness1), (child2, fitness2)]
        # print("in crossover",offsprings[0])
        return offsprings

    def mutate(self,chromosome):

        new_chromosome = chromosome[0].copy()
        fitness = chromosome[1]
        r = np.random.random()

        if r<self.mutation_rate:
            # print(chromosome)
            new_chromosome.pop()
            # Perform mutation by adding a new polygon to the chromosome
            x = [random.randint(0, self.canvas_size[0]) for i in range(3)]
            y = [random.randint(0, self.canvas_size[1]) for i in range(3)]
            color = (random.random(), random.random(), random.random(), random.random())
            new_chromosome.append({'x': x, 'y': y, 'color': color})
            fitness = self.calculate_fitness(new_chromosome)

        return (new_chromosome, fitness)

    def random_chromosome(self):
        num_polygons = 5
        polygons = []
        for i in range(num_polygons):
            x = [random.randint(0, self.canvas_size[0]) for j in range(3)]
            y = [random.randint(0, self.canvas_size[1]) for j in range(3)]
            color = (random.random(), random.random(), random.random(), random.random())
            # color = 'blue'
            polygons.append({'x': x, 'y': y, 'color': color})
        # self.plot_polygons(polygons)
        fitness = self.calculate_fitness(polygons)
        # print("printing random chromosome",fitness)
        # print("printing random chromosome",polygons)
        return (polygons, fitness)


    def plot_polygons(self,polygons):
        fig, ax = plt.subplots(figsize=(self.canvas_size[0]/100, self.canvas_size[1]/100), facecolor='black')  
        ax.set_xlim(0, self.canvas_size[0])
        ax.set_ylim(0, self.canvas_size[1])
        ax.set_aspect('equal', 'box')

        for polygon in polygons:
            try:
                x = polygon['x']
            except:
                print(polygon)
            x = polygon['x']
            y = polygon['y']
            color = polygon['color']

            poly = Polygon(np.column_stack([x, y]), closed=True, facecolor=color, edgecolor='none')
            ax.add_patch(poly)

        ax.axis('off')  
        ax.grid(False)  

        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)  # Adjust subplots to fill the entire figure area

        buffer = io.BytesIO()  # Create a buffer to save the image
        plt.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0, facecolor='black', transparent=True)
        buffer.seek(0)

        img = Image.open(buffer)
        img = img.resize(self.canvas_size)  # Resize the image to the desired size
        img_array = np.array(img)

        save_path = os.path.join(os.getcwd(), "gen_mona.png")

        plt.savefig(save_path, bbox_inches='tight', pad_inches=0, facecolor=fig.get_facecolor(), transparent=True)
        # plt.show()

        plt.close(fig)  # Close the figure to free up memory

        return img_array


def plot_polygons(polygons, canvas_size=(100, 100)):
    print(polygons)
    fig, ax = plt.subplots()
    ax.set_xlim(0, canvas_size[0])
    ax.set_ylim(0, canvas_size[1])
    ax.set_aspect('equal', 'box')

    for polygon in polygons:
        x = polygon['x']
        y = polygon['y']
        color = polygon['color']

        poly = Polygon(np.column_stack([x, y]), closed=True, facecolor=color, edgecolor='none')
        ax.add_patch(poly)

    ax.axis('off')  # Turn off the axis
    ax.grid(False)  # Turn off the grid lines

    plt.show()
# Example usage
polygon = [{'x': [1, 26, 4], 'y': [24, 53, 87], 'color': 'blue'}, {'x': [38, 28, 11], 'y': [16, 37, 63], 'color': 'blue'}, {'x': [70, 21, 29], 'y': [37, 28, 77], 'color': 'blue'}, {'x': [78, 83, 53], 'y': [77, 13, 10], 'color': 'blue'}, {'x': [41, 90, 4], 'y': [99, 15, 98], 'color': 'blue'}]
# plot_polygons(polygon)

