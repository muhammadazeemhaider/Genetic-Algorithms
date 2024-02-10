import random
from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from problem import Problem
import cv2

class MonaLisa(Problem):

    def __init__(self, population_size, offspring_size, generations, mutation_rate, iterations, filename):
        self.original_image = Image.open(filename)
        super().__init__(population_size, offspring_size, generations, mutation_rate, iterations, filename)
        
    def calculate_fitness(self, chromosome):
        original_pixels = np.array(self.original_image)

        test_image = Image.new('RGB', self.original_image.size)
        draw = ImageDraw.Draw(test_image)
        # plt.imshow(draw)
        for polygon in chromosome:
            x = polygon['x']
            y = polygon['y']
            color =  tuple(int(c * 255) for c in polygon['color'])

            poly = [(x[i], y[i]) for i in range(len(x))]
            draw.polygon(poly, fill=color)

        plt.imshow(test_image)
        test_pixels = np.array(test_image)

        # Ensure the dimensions match and convert to same datatype for error calculation
        original_pixels = original_pixels.astype(np.float32)
        test_pixels = test_pixels.astype(np.float32)
        print("printing from fitness function")
        plt.imshow(test_pixels)
        print("plotting done")
        # Normalize pixel values
        original_pixels /= 255.0
        test_pixels /= 255.0

        # Calculate Mean Squared Error
        mse = np.mean((original_pixels - test_pixels) ** 2)
        print(mse)
        return mse
    
    def crossover(self, parent1, parent2):
        # Perform crossover to create a new chromosome from two parents
        crossover_point = random.randint(1, len(parent1))

        # Create a new chromosome by combining parts of both parents
        child1 = parent1[0][:crossover_point] + parent2[0][crossover_point:]
        child2 = parent2[0][:crossover_point] + parent1[0][crossover_point:]

        # print("printing child1",type(child1))
        fitness1 = self.calculate_fitness(child1)
        fitness2 = self.calculate_fitness(child2)

        offsprings = [(child1, fitness1), (child2, fitness2)]
        return offsprings

    def mutate(self,chromosome):
        # Perform mutation by adding a random polygon to the chromosome
        new_chromosome = chromosome[0].copy()

        # Choose a random polygon to mutate
        if random.random() < self.mutation_rate:
            num_polygons = len(new_chromosome)

            polygon_index = random.randint(0, num_polygons - 1)
            new_chromosome[polygon_index] = self.random_polygon()

            fitness = self.calculate_fitness(new_chromosome)
            new_chromosome = (new_chromosome, fitness)
            return new_chromosome
        else:
            return chromosome

    def random_chromosome(self):
        print("generating random chromosome")
        # Generate a random chromosome for the Mona Lisa problem
        num_polygons = 5
        polygons = []
        for i in range(num_polygons):
            polygon = self.random_polygon()
            polygons.append(polygon)
        self.plot_polygons(polygons)
        fitness = self.calculate_fitness(polygons)
        # print("printing random chromosome",fitness)
        return (polygons, fitness)
    
    def random_polygon(self):
        self.canvas_size = self.original_image.size
        # Generate a random polygon for the Mona Lisa problem
        x = [random.randint(0, self.canvas_size[0]) for j in range(3)]
        y = [random.randint(0, self.canvas_size[1]) for j in range(3)]
        color = (random.random(), random.random(), random.random(), random.random())
        return {'x': x, 'y': y, 'color': color}

    def plot_polygons(self, polygons):
        print(polygons)
        fig, ax = plt.subplots(facecolor='black')  # Set the facecolor of the figure to black
        ax.set_xlim(0, self.canvas_size[0])
        ax.set_ylim(0, self.canvas_size[1])
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