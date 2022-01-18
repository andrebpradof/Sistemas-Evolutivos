import numpy as np
from random import randrange, seed
import json

MAX_POPULATION = 50
F_PROBABILITY = 0.5
MUTATION_RATE = 1


def createBoard(n):
    board = np.zeros([n, n], dtype=int)
    return board


def cleanBoard(board, n):
    board = np.zeros([n, n], dtype=int)
    return board


def initializesPopulation(n):
    population = np.zeros([MAX_POPULATION, n], dtype=int)
    for i in range(MAX_POPULATION):
        for j in range(n):
            population[i][j] = randrange(start=0, stop=n)
    return population


def generateFitnessVector(population, board, n):
    fitness_population = np.zeros(MAX_POPULATION, dtype=int)
    for i in range(MAX_POPULATION):
        fitness_population[i], board = valuationSample(board, population[i], n)
    return fitness_population, board


def recombinesTournamentIndividuals(population, n, fitness):
    indexBetterFitness = 0
    betterFitness = 0
    for i in range(MAX_POPULATION):
        if(fitness[i] < betterFitness):
            indexBetterFitness = i
            betterFitness = fitness[i]

    newPopulation = initializesPopulation(n)
    for i in range(n):
        newPopulation[0][i] = population[indexBetterFitness][i]

    for i in range(1, MAX_POPULATION):
        fatherA = selectFather(fitness)
        fatherB = selectFather(fitness)

        limit = randrange(start=0, stop=n)

        for j in range(limit):
            newPopulation[i][j] = population[fatherA][j]

        for j in range(limit, n):
            newPopulation[i][j] = population[fatherB][j]

    return newPopulation, indexBetterFitness


def selectFather(fitness):
    indA = randrange(start=0, stop=MAX_POPULATION)
    indB = randrange(start=0, stop=MAX_POPULATION)

    num = (randrange(start=0, stop=1000))/1000.0

    if(num < F_PROBABILITY):
        if (fitness[indA] > fitness[indB]):
            return indA
        else:
            return indB
    else:
        if (fitness[indA] < fitness[indB]):
            return indA
        else:
            return indB


def recombinesIndividualsElitism(population, n, fitness):
    indexBetterFitness = 0
    betterFitness = 100000000

    for i in range(MAX_POPULATION):
        if(fitness[i] < betterFitness):
            indexBetterFitness = i
            betterFitness = fitness[i]

    for i in range(MAX_POPULATION):
        for j in range(n):
            population[i][j] = population[indexBetterFitness][j]

    # VERIFICAR RETTORNO AQUIIII
    return indexBetterFitness, population


def mutation(population, n, mutationRate):
    for i in range(MAX_POPULATION):
        if((randrange(start=0, stop=1000)/1000.0) <= MUTATION_RATE):
            for j in range(mutationRate):
                genome = randrange(start=0, stop=n)
                if(population[i][genome] == 0):
                    population[i][genome] += 1
                elif(population[i][genome] == n-1):
                    population[i][genome] -= 1
                elif(randrange(start=0, stop=2)):
                    population[i][genome] += 1
                else:
                    population[i][genome] -= 1
    return population


def randomFeeding(n):
    vector = [randrange(start=0, stop=n) for i in range(n)]
    return vector


def valuationSample(board, sample, n):
    sumFitness = 0
    atk = 0
    board = cleanBoard(board, n)
    for i in range(n):
        board = insertPiece(board, i, sample[i], 1)
    for i in range(n):
        atk, board = verifyAttack(board, n, i, sample[i])
        sumFitness += atk
        board = removePiece(board, i, sample[i])
    return sumFitness, board


def insertSample(sample, board, n):
    for i in range(n):
        board[i][sample[i]] = 1
    return board


def insertPiece(board, position_X, position_Y, typePiece):
    if board[position_X][position_Y] != 0:
        return -1
    board[position_X][position_Y] = typePiece

    return board


def removePiece(board, position_X, position_Y):
    if board[position_X][position_Y] == 0:
        return -1
    board[position_X][position_Y] = 0

    return board


def verifyAttack(board, n, position_X, position_Y):
    atk = 0
    typeCheck = board[position_X][position_Y]

    if position_X >= n or position_Y >= n:
        return -1

    if typeCheck == 1 or typeCheck == 2:
        for i in range(n):
            if i == position_Y:
                continue
            if board[position_X][i] != 0:
                atk += 1
        for i in range(n):
            if i == position_X:
                continue
            if board[i][position_Y] != 0:
                atk += 1
        # for i in range(n):
        #     if board[position_X][i] != 0 and i != position_Y:
        #         atk += 1
        # for i in range(n):
        #     if board[i][position_Y] != 0 and i != position_X:
        #         atk += 1

    if typeCheck == 1 or typeCheck == 3:
        i = 1
        while (position_X + i < n) and (position_Y + i < n):
            if board[position_X + i][position_Y + i] != 0:
                atk += 1
            i += 1
        i = 1
        while (position_X - i >= 0) and (position_Y - i >= 0):
            if board[position_X - i][position_Y - i] != 0:
                atk += 1
            i += 1
        i = 1
        while (position_X + i < n) and (position_Y - i >= 0):
            if board[position_X + i][position_Y - i] != 0:
                atk += 1
            i += 1
        i = 1
        while (position_X - i >= 0) and (position_Y + i < n):
            if board[position_X - i][position_Y + i] != 0:
                atk += 1
            i += 1

    return atk, board


def printBoard(board, n):
    for i in range(n):
        for j in range(n):
            print(" ", board[i][j], " ", end="")
        print("")


def generateFileBoard(board, n, generation, stingJson, end, genocide, fitness):
    boardJson = '"'+str(generation) + \
        '" : { "genocidio": '+str(genocide) + \
        ', "fitness": '+str(fitness)+', "board": ['
    dictionary = ""
    for i in range(n):
        for j in range(n):
            if board[i][j] == 1:
                # print(i, j, end="")
                dictionary = dictionary+'{"row": '+str(i)+',"col": '+str(j)+'}'
                if i != (n-1):
                    dictionary = dictionary+","

    boardJson = boardJson+dictionary+'] }'
    if end == 1:
        boardJson = boardJson+','
    stingJson = stingJson+boardJson
    return stingJson


def generateFileJson(stingJson):
    stingJson = stingJson+"}"
    json_object = json.loads(stingJson)
    with open("sample.json", "w") as outfile:
        json.dump(json_object, outfile)


def printPopulation(population, n):
    for i in range(MAX_POPULATION):
        for j in range(n):
            print(" ", population[i][j], " ", end="")
        print("")


def main():
    # seed(7)
    #print("Type the dimension n desired for the board: ")
    n = 10
    board = createBoard(n)
    genocides = 0
    stop_criterion = 1
    best_individual = np.zeros(n, dtype=int)
    generation = 0
    mutation_rate = 1
    fitness_previous = 1000000
    stingJson = '{'

    while stop_criterion:
        population = initializesPopulation(n)
        if generation > 0:
            if randrange(start=0, stop=2):
                for i in range(n):
                    population[0][i] = best_individual[i]
        while True:
            fitness, board = generateFitnessVector(population, board, n)
            #population, index_best_individual = recombinesTournamentIndividuals(population, n, fitness)
            index_best_individual, population = recombinesIndividualsElitism(
                population, n, fitness)
            for i in range(n):
                best_individual[i] = population[index_best_individual][i]
            population = mutation(population, n, mutation_rate)
            board = cleanBoard(board, n)
            board = insertSample(population[index_best_individual], board, n)
            # printBoard(board, n)

            boardAnt = board
            generation += 1

            fitness_best_individual, board = valuationSample(
                board, best_individual, n)

            # print("Generation: ", generation)
            #print("fitness: ",fitness_best_individual)

            if fitness_best_individual == 0:
                board = insertSample(best_individual, board, n)
                printBoard(board, n)

                stingJson = generateFileBoard(
                    board, n, generation, stingJson, 0, 0, fitness_best_individual)
                # print(stingJson)

                generateFileJson(stingJson)

                print("Generation: ", generation)
                print("genocidios: ", genocides)
                print("fitness: ", fitness_best_individual)
                stop_criterion = 0
                break
            if fitness_best_individual == fitness_previous:
                mutation_rate += 1
            elif fitness_best_individual < fitness_previous:
                mutation_rate = 0
            fitness_previous = fitness_best_individual

            if mutation_rate == n:
                genocides += 1
                mutation_rate = 1
                population = 0

                stingJson = generateFileBoard(
                    boardAnt, n, generation, stingJson, 1, 1, fitness_best_individual)

                break
            else:
                stingJson = generateFileBoard(
                    boardAnt, n, generation, stingJson, 1, 0, fitness_best_individual)

    print("End")
    return 0


if __name__ == "__main__":
    main()
