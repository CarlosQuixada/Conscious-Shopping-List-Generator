import random

import numpy
from deap import base, creator, algorithms, tools

from app.model.dream import Dream


class GeneticAlgorithm:
    def __init__(self, limit_spent, list_dreams):
        self.__probability_crossover = 0.9
        self.__probability_mutation = 0.01
        self.__number_generations = 100

        self.__limit_spent = limit_spent
        self.__dreams, self.values = self.__create_dream(list_dreams)

        self.__toolbox = self.__deap_boot(self.__dreams)

    def __evaluation(self, individual):
        """
            Method of evaluation of the individuals in the generations of the genetic algorithm
        :param individual: individual of the generation
        :return:individual rank value
        """

        amount_dreams = 0
        sum_prices = 0

        for i in range(len(individual)):
            if individual[i] == 1:
                amount_dreams += 1
                sum_prices += self.values[i]

        if sum_prices > self.__limit_spent:
            amount_dreams = 1

        return amount_dreams / 100000,

    def __create_dream(self, list_dreams):
        """
            Method responsible for turning json dreams to object
        :param list_dreams: dream list in json
        :return: dream object list and dream price list
        """

        dreams = []
        for dream in list_dreams:
            dreams.append(Dream(dream['name'], dream['price']))

        values = [dream.price for dream in dreams]

        return dreams, values

    def __deap_boot(self, dreams):
        """
            Method responsible for lib deap initialization
        :param dreams: dream list
        :return: toolbox
        """

        random.seed(1)
        toolbox = base.Toolbox()

        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)

        toolbox.register("attr_bool", random.randint, 0, 1)
        toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=len(dreams))
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        toolbox.register("evaluate", self.__evaluation)
        toolbox.register("mate", tools.cxOnePoint)
        toolbox.register("mutate", tools.mutFlipBit, indpb=0.01)
        toolbox.register("select", tools.selRoulette)

        return toolbox

    def __create_response(self, best):
        """
            Method responsible for creating json purchase suggestion response
        :param best: The best suggestion found by the algorithm
        :return: suggestion list in json
        """

        suggestion = []

        for individuo in best:
            for i in range(len(self.__dreams)):
                if individuo[i] == 1:
                    suggestion.append({'name': self.__dreams[i].name, 'price': self.__dreams[i].price})

        return {'suggestion': suggestion}

    def __create_statistic(self):
        """
            Method responsible for initializing the statistics used in the genetic algorithm.
        :return: initialized statistic
        """

        statistic = tools.Statistics(key=lambda individuo: individuo.fitness.values)
        statistic.register("max", numpy.max)
        statistic.register("min", numpy.min)
        statistic.register("med", numpy.mean)
        statistic.register("std", numpy.std)

        return statistic

    def generate_list(self):
        """
            Method responsible for executing purchase suggestion list generation.
        :return: Json with the cuelist
        """

        group = self.__toolbox.population(n=20)

        statistic = self.__create_statistic()
        group, info = algorithms.eaSimple(group, self.__toolbox, self.__probability_crossover,
                                          self.__probability_mutation, self.__number_generations, statistic)

        best = tools.selBest(group, 1)
        response = self.__create_response(best)

        return response
