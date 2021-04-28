import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_distance(self, city):
        a = abs(self.x - city.x)
        b = abs(self.y - city.y)
        return np.sqrt(a ** 2 + b ** 2)


class Fitness:
    def __init__(self, route):
        self.distance = 0.0
        self.fitness = 0.0
        self.route = route

    def get_dist(self):
        if self.distance == 0:
            self.calc_dist()
        return self.distance

    def get_fitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.get_dist())
        return self.fitness

    def calc_dist(self):
        path_distance = 0
        iterator = iter(self.route)
        for i in iterator:
            from_city = next(iterator, None)
            to_city = next(iterator, None)
            if(from_city is not None and to_city is not None):
                path_distance += from_city.get_distance(to_city)
        self.distance = path_distance


class TravelingSalesman:

    def __init__(self, n, mutation_rate=0.01, elite_size=20, generations=500, pop_size=100):
        self.n = n
        self.mutation_rate = mutation_rate
        self.elite_size = elite_size
        self.generations = generations
        self.pop_size = pop_size
        self.cities = self.generate_random_cities()
        self.gen_to_print = [(n//5 * i) + 10 for i in range(1, 4)]
        self.gen_to_print.append(10)

    def generate_random_cities(self):
        return [City(random.randint(1, 300), random.randint(1, 300)) for i in range(self.n)]

    def create_route(self):
        return random.sample(self.cities, self.n)

    def initial_population(self):
        return [self.create_route() for i in range(self.pop_size)]

    def rank_routes(self, population):
        results = {index: Fitness(route).get_fitness()
                   for index, route in enumerate(population)}
        return sorted(results.items(), key=lambda x: x[1], reverse=True)

    def selection(self, pop_ranked):
        total = sum(n for _, n in pop_ranked)
        part_of_whole = [route[1] / total for route in pop_ranked]

        results = [pop_ranked[i][0] for i in range(self.elite_size)]

        for i in range(len(pop_ranked) - self.elite_size):
            radom_route_based_on_fitness = np.random.choice(
                len(part_of_whole), p=part_of_whole)
            results.append(pop_ranked[radom_route_based_on_fitness][0])
        return results

    def breed(self, parent1, parent2):
        gene_a = random.randint(0, len(parent1))
        gene_b = random.randint(0, len(parent1))

        start = min(gene_a, gene_b)
        end = max(gene_a, gene_b)

        child1 = [parent1[i] for i in range(start, end)]
        child2 = [city for city in parent2 if city not in child1]

        return child1 + child2

    def breed_population(self, matingpool):
        length = len(matingpool) - self.elite_size
        pool = random.sample(matingpool, len(matingpool))

        children = [matingpool[i] for i in range(self.elite_size)]

        for i in range(length):
            child = self.breed(pool[i], pool[len(matingpool) - i - 1])
            children.append(child)
        return children

    def mutate(self, individual):
        for swapped in range(len(individual)):
            if(random.random() < self.mutation_rate):
                swapWith = random.randint(0, len(individual) - 1)
                temp = individual[swapped]
                individual[swapped] = individual[swapWith]
                individual[swapWith] = temp
        return individual

    def mutate_population(self, population):
        return [self.mutate(individual) for individual in population]

    def get_next_generation(self, current_gen):
        pop_ranked = self.rank_routes(current_gen)
        selections = self.selection(pop_ranked)
        matingpool = [current_gen[selection] for selection in selections]
        children = self.breed_population(matingpool)
        next_gen = self.mutate_population(children)
        return next_gen

    def genetic_algorithm(self):
        pop = self.initial_population()

        #print("Initial distance: " + str(1 / self.rank_routes(pop)[0][1]))
        for i in range(self.generations):
            if(i in self.gen_to_print):
                print("Distance: at gen " + str(i) + " : " +
                      str(1 / self.rank_routes(pop)[0][1]))
            pop = self.get_next_generation(pop)

        print("Final distance: " + str(1 / self.rank_routes(pop)[0][1]))
        best_route_index = self.rank_routes(pop)[0][0]
        best_route = pop[best_route_index]
        return best_route


if __name__ == "__main__":
    print('Enter n:')
    n = int(input())
    if n <= 100:
        salesman = TravelingSalesman(n)
        salesman.genetic_algorithm()
    else:
        print('n should not be more than 100')
