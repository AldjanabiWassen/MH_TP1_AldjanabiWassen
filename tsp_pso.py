import math
import random
import matplotlib.pyplot as plt


"""
- the classe city represent object of type city 
- __init__ constructor of OOP
- distance to calculate the euclidienne distance

"""
class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, city):
        return math.hypot(self.x - city.x, self.y - city.y)

    def __repr__(self):
        return f"({self.x}, {self.y})"


"""
- read_cities to read the data
in every iteration(38 in my data) it create an object of type city with an x and y
and put them in array called citier a return it

"""

def read_cities(size):
    cities = []
    with open(f'data.txt', 'r') as handle:
        lines = handle.readlines()
        for line in lines:
            x, y = map(float, line.strip().split())
            cities.append(City(x, y))
    return cities

"""
path_cost calculate the cost of a path
"""
def path_cost(route):
    return sum([city.distance(route[index - 1]) for index, city in enumerate(route)])

"""
vistualize_tsp for vistualization of plots
"""
def visualize_tsp(title, cities):
    fig = plt.figure()
    fig.suptitle(title)
    x_list, y_list = [], []
    for city in cities:
        x_list.append(city.x)
        y_list.append(city.y)
    x_list.append(cities[0].x)
    y_list.append(cities[0].y)

    plt.plot(x_list, y_list, 'ro')
    plt.plot(x_list, y_list, 'g')
    plt.show(block=True)


"""
in this part we begin the implemantation of PSO 
we implemante the classe Particle with an object with two attribut:
route : path chosen by the particle
velocity. 

- clear_velocity clear the array 
- update_costs_and_pbest do the update of attribut of object particle
if the current_cost is less then pbest_cost the then pbest_cost will be the current_cost and that means that 
the particle has found a better cost then that she had and make update

"""

class Particle:
    def __init__(self, route, cost=None):
        self.route = route
        self.pbest = route
        self.current_cost = cost if cost else self.path_cost()
        self.pbest_cost = cost if cost else self.path_cost()
        self.velocity = []

    def clear_velocity(self):
        self.velocity.clear()

    def update_costs_and_pbest(self):
        self.current_cost = self.path_cost()
        if self.current_cost < self.pbest_cost:
            self.pbest = self.route
            self.pbest_cost = self.current_cost

    def path_cost(self):
        return path_cost(self.route)



"""

in this class we implement the PSO algorithm

- _init_ we have iterations (epoch) that's the number of iteration
- population_size : nuber of particle

"""


class PSO:

    def __init__(self, iterations, population_size, gbest_probability=1.0, pbest_probability=1.0, cities=None):
        self.cities = cities
        self.gbest = None
        self.gcost_iter = []
        self.iterations = iterations
        self.population_size = population_size
        self.particles = []
        self.gbest_probability = gbest_probability
        self.pbest_probability = pbest_probability

        solutions = self.initial_population() # here we init the object PSO hna ninitialisiw l'Objet PSO with a random population
        # the number of path will be the number of solution
        # then we create particle object and we give one of the paths from the methode initial_population  
        # 
        self.particles = [Particle(route=solution) for solution in solutions]

    """
    random_route return an array o object city (give as un path between our city)
    """
    def random_route(self):
        return random.sample(self.cities, len(self.cities))

    def initial_population(self):
        #random population hiya anou ykheyer des routes randomly (le nombre ta3hom houwa le population_size)
        random_population = [self.random_route() for _ in range(self.population_size - 1)]
        greedy_population = [self.greedy_route(0)]
        return [*random_population, *greedy_population]
        # return [*random_population]

    """
    in this algorith they use greedy algorithm for better result 

    """

    def greedy_route(self, start_index):
        unvisited = self.cities[:]
        del unvisited[start_index]
        route = [self.cities[start_index]]
        while len(unvisited):
            index, nearest_city = min(enumerate(unvisited), key=lambda item: item[1].distance(route[-1]))
            route.append(nearest_city)
            del unvisited[index]
        return route

    def run(self):
        """

        """
        self.gbest = min(self.particles, key=lambda p: p.pbest_cost)
        print(f"initial cost is {self.gbest.pbest_cost}")
        plt.ion()
        plt.draw()
        for t in range(self.iterations):
            self.gbest = min(self.particles, key=lambda p: p.pbest_cost)
            if t % 20 == 0:
                plt.figure(0)
                plt.plot(pso.gcost_iter, 'g')
                plt.ylabel('Distance')
                plt.xlabel('Generation')
                fig = plt.figure(0)
                fig.suptitle('pso iter')
                x_list, y_list = [], []
                for city in self.gbest.pbest:
                    x_list.append(city.x)
                    y_list.append(city.y)
                x_list.append(pso.gbest.pbest[0].x)
                y_list.append(pso.gbest.pbest[0].y)
                fig = plt.figure(1)
                fig.clear()
                fig.suptitle(f'pso TSP iter {t}')

                plt.plot(x_list, y_list, 'ro')
                plt.plot(x_list, y_list, 'g')
                plt.draw()
                plt.pause(.001)
            self.gcost_iter.append(self.gbest.pbest_cost)


            """
            
            """
            for particle in self.particles:
                particle.clear_velocity()
                temp_velocity = []
                gbest = self.gbest.pbest[:]
                new_route = particle.route[:]

                for i in range(len(self.cities)):
                    if new_route[i] != particle.pbest[i]:
                        swap = (i, particle.pbest.index(new_route[i]), self.pbest_probability)
                        temp_velocity.append(swap)
                        new_route[swap[0]], new_route[swap[1]] = \
                            new_route[swap[1]], new_route[swap[0]]

                for i in range(len(self.cities)):
                    if new_route[i] != gbest[i]:
                        swap = (i, gbest.index(new_route[i]), self.gbest_probability)
                        temp_velocity.append(swap)
                        gbest[swap[0]], gbest[swap[1]] = gbest[swap[1]], gbest[swap[0]]

                particle.velocity = temp_velocity

                for swap in temp_velocity:
                    if random.random() <= swap[2]:
                        new_route[swap[0]], new_route[swap[1]] = \
                            new_route[swap[1]], new_route[swap[0]]

                """
                in the end we update the pbest_cost and give the particle a new route 
                
                """
                particle.route = new_route
                particle.update_costs_and_pbest()


if __name__ == "__main__":
    # hadi ghir bach na9raw le fichier data ta3na
    cities = read_cities(38)
    # hadi l'initialisation ta3 l'objet PSO, t9edri tla3bi b les parametres hadou machi mouchkil, hadi yssamouha etude parametrique ida rani 
    # chafi bien 
    pso = PSO(iterations=1400, population_size=1000, pbest_probability=0.9, gbest_probability=0.02, cities=cities)
    pso.run() # this is magic! hhhhhh
    # ki ykamel l'execution nafichiw le pbest_cost ta3na l pbest hi houwa hadik la liste ta3 les (X, Y) ta3 la route optimale
    print(f'cost: {pso.gbest.pbest_cost}\t| gbest: {pso.gbest.pbest}')

    x_list, y_list = [], []
    for city in pso.gbest.pbest:
        x_list.append(city.x)
        y_list.append(city.y)
    x_list.append(pso.gbest.pbest[0].x)
    y_list.append(pso.gbest.pbest[0].y)
    fig = plt.figure(1)
    fig.suptitle('pso TSP')

    plt.plot(x_list, y_list, 'ro')
    plt.plot(x_list, y_list)
    plt.show(block=True)