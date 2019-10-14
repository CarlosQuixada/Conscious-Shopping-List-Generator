import random

import numpy
from deap import base, creator, algorithms, tools

from app.model.dream import Dream


class GeneticAlgorithm:
    def __init__(self, limit_spent, list_dreams):
        self.probability_crossover = 0.9
        self.probability_mutacao = 0.01
        self.numero_geracoes = 100

        self.limit_spent = limit_spent
        self.dreams, self.values = self.__create_dream(list_dreams)

        self.creator, self.toolbox = self.__deap_boot(self.dreams)

    def __evaluation(self, individual):
        amount_dreams = 0
        sum_prices = 0

        for i in range(len(individual)):
            if individual[i] == 1:
                amount_dreams += 1
                sum_prices += self.values[i]

        if sum_prices > self.limit_spent:
            amount_dreams = 1

        return amount_dreams / 100000,

    def __create_dream(self, list_dreams):
        dreams = []
        for dream in list_dreams:
            dreams.append(Dream(dream['name'], dream['value']))

        values = [dream.value for dream in dreams]

        return dreams, values

    def __deap_boot(self, dreams):
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

        return creator, toolbox

    def create_response(self, best):
        suggestion = []

        for individuo in best:
            for i in range(len(self.dreams)):
                if individuo[i] == 1:
                    suggestion.append({'name': self.dreams[i].name, 'price': self.dreams[i].value})

        return {'suggestion': suggestion}

    def __create_statistic(self):
        statistic = tools.Statistics(key=lambda individuo: individuo.fitness.values)
        statistic.register("max", numpy.max)
        statistic.register("min", numpy.min)
        statistic.register("med", numpy.mean)
        statistic.register("std", numpy.std)

        return statistic

    def generate_list(self):

        group = self.toolbox.population(n=20)

        statistic = self.__create_statistic()
        group, info = algorithms.eaSimple(group, self.toolbox, self.probability_crossover,
                                          self.probability_mutacao, self.numero_geracoes, statistic)

        best = tools.selBest(group, 1)
        response = self.create_response(best)

        return response
