import numpy as np
from random import randrange, seed

MAX_POPULATION = 50

def criateBoard(n):
    board = np.zeros((n, n))
    return board


def cleanBoard(board, n):
    board = np.zeros((n, n))
    return board


def initializesPopulation(n):
    population = np.zeros(MAX_POPULATION,n)
    for i in range(MAX_POPULATION):
        for j in range(n):
            population[i][j] = randrange(start=0,stop=n)
    return population

#####################################################
def assessIndividual(board, population,n):
    fitness_sum = 0
    cleanBoard(board)
    #for i in range(n):


def generateFitnessVector(population, board, n):
    fitness_population = np.zeros(MAX_POPULATION)
    for i in range(MAX_POPULATION):
        fitness_population[i] = assessIndividual(board, population[i],n)
###########################################    

def main():
    seed(7)
    #print("Type the dimension n desired for the board: ")
    n = 10
    board = criateBoard(n)
    genocides = 0
    stop_criterion = 1
    best_individual = np.zeros(n)
    generation = 0
    mutation_rate = 1
    fitness_previous = 1000000

    while stop_criterion:
        population = initializesPopulation(n)
        if generation > 0:
            for i in range(n):
                population[0][i] = best_individual[i]
        while True:
            fitness = generateFitnessVector(population,board,n)

if __name__ == "__main__":
    main()