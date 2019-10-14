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

    # def __create_statistic(self):

    # statistic.register("min", numpy.min)
    # statistic.register("med", numpy.mean)
    # statistic.register("std", numpy.std)

    #    return statistic, tools

    def generate_list(self):
        toolbox = base.Toolbox()

        creator.create("FitnessMax", base.Fitness, weights=(1.0,))

        creator.create("Individual", list, fitness=creator.FitnessMax)
        toolbox.register("attr_bool", random.randint, 0, 1)
        toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=len(self.dreams))
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        toolbox.register("evaluate", self.__evaluation)
        toolbox.register("mate", tools.cxOnePoint)
        toolbox.register("mutate", tools.mutFlipBit, indpb=0.01)
        toolbox.register("select", tools.selRoulette)

        populacao = toolbox.population(n=20)

        probabilidade_crossover = 0.9

        probabilidade_mutacao = 0.01

        numero_geracoes = 100

        estatisticas = tools.Statistics(key=lambda individuo: individuo.fitness.values)
        estatisticas.register("max", numpy.max)
        estatisticas.register("min", numpy.min)
        estatisticas.register("med", numpy.mean)
        estatisticas.register("std", numpy.std)

        populacao, info = algorithms.eaSimple(populacao, toolbox,
                                              probabilidade_crossover,
                                              probabilidade_mutacao,
                                              numero_geracoes, estatisticas)

        melhores = tools.selBest(populacao, 1)
        for individuo in melhores:
            soma = 0
            for i in range(len(self.dreams)):
                if individuo[i] == 1:
                    soma += self.values[i]
                    print("Nome: %s R$ %s " % (self.dreams[i].name, self.dreams[i].value))
            print("Melhor solução: %s" % soma)

        return "Lengaaaaaall"
