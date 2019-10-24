import sys
sys.path.append('../aima-python')
sys.path.append('../libs')
import random
import numpy
from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from problems import *

#Problem size
NB_QUEENS = 50

MATING_PROB = 0.1
MUTATING_PROB = 0.7
N_GENERATIONS = 50

SELECTION_SIZE = 15

# This function was found on internet. I cannot understand how it works, thats the reason i do not use it.
# However, it drastically increase the efficiency
def evaluate_queens(individual):
    """Evaluation function for the n-queens problem.
    The problem is to determine a configuration of n queens
    on a nxn chessboard such that no queen can be taken by
    one another. In this version, each queens is assigned
    to one column, and only one queen can be on each line.
    The evaluation function therefore only counts the number
    of conflicts along the diagonals.
    """
    size = len(individual)
    #Count the number of conflicts with other queens.
    #The conflicts can only be diagonal, count on each diagonal line
    left_diagonal = [0] * (2*size-1)
    right_diagonal = [0] * (2*size-1)
    
    #Sum the number of queens on each diagonal:
    for i in range(size):
        left_diagonal[i+individual[i]] += 1
        right_diagonal[size-1-i+individual[i]] += 1
    
    #Count the number of conflicts on each diagonal
    sum_ = 0
    for i in range(2*size-1):
        if left_diagonal[i] > 1:
            sum_ += left_diagonal[i] - 1
        if right_diagonal[i] > 1:
            sum_ += right_diagonal[i] - 1
    return sum_,

def count_conflicts_2(individual):
    conflicts = 0

    # Creates bidimensional board
    board = [[0 for i in range(NB_QUEENS)]] * NB_QUEENS
    for i in range(NB_QUEENS):
        board[i][individual[i]] = 1

    # Creates an array with the diagonals
    diagonals = []
    for k in range(NB_QUEENS):
        diagonals.append([board[i][j] for i in range(NB_QUEENS) for j in range(NB_QUEENS) if i+k==j])
        diagonals.append([board[i][j] for i in range(NB_QUEENS) for j in range(NB_QUEENS) if i==j+k])

    # Erase from the array the first element becouse its duplicated
    diagonals = diagonals[1:]
    # Sum each diagonal queens
    diagonal_sums = [sum(d) for d in diagonals]
    # Sum 1 for each sum if its greater than one queen
    conflicts = sum(1 for s in diagonal_sums if s > 1)
    return (conflicts,)

def count_conflicts(individual):
    # Creates bidimensional board
    board = [[0 for j in range(len(individual))] for i in range(len(individual))]
    for i in range(len(individual)):
        board[i][individual[i]] = 1

    # create array from state
    array_board = numpy.array(board)
    
    # array_board.diagonal returns the top-left-to-lower-right diagonal "i"
    # according to this diagram:
    #
    #  0  1  2  3  4 ...
    # -1  0  1  2  3
    # -2 -1  0  1  2
    # -3 -2 -1  0  1
    #  :
    #
    # You wanted lower-left-to-upper-right and upper-left-to-lower-right diagonals.
    #
    # The syntax a[slice,slice] returns a new array with elements from the sliced ranges,
    # where "slice" is Python's [start[:stop[:step]] format.
    
    # "::-1" returns the rows in reverse. ":" returns the columns as is,
    # effectively vertically mirroring the original array so the wanted diagonals are
    # lower-right-to-uppper-left.
    #
    # Then a list comprehension is used to collect all the diagonals.  The range
    # is -x+1 to y (exclusive of y), so for a matrix like the example above
    # (x,y) = (4,5) = -3 to 4.
    diags = [array_board[::-1,:].diagonal(i) for i in range(-array_board.shape[0]+1,array_board.shape[1])]

    # Now back to the original array to get the upper-left-to-lower-right diagonals,
    # starting from the right, so the range needed for shape (x,y) was y-1 to -x+1 descending.
    diags.extend(array_board.diagonal(i) for i in range(array_board.shape[1]-1,-array_board.shape[0],-1))

    # Another list comp to convert back to Python lists from numpy arrays,
    # so it prints what you requested.
    diagonals = [n.tolist() for n in diags]
    return (sum(1 for d in diagonals if sum(d) > 1),)
    
# The fitness values are set
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
# An indidual is a lista that contains a fitness function
creator.create("Individual", list, fitness=creator.FitnessMin)

# For permutation, random.sample() is used
toolbox = base.Toolbox()
toolbox.register("permutation", random.sample, range(NB_QUEENS), NB_QUEENS)

# The individual function is registered so it can return a new individual through permutation
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.permutation)
# The population function is registered so it can return a list of individuals
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# The evaluate function is set as the function that counts conflicts
toolbox.register("evaluate", count_conflicts)
toolbox.register("mate", tools.cxPartialyMatched)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=2.0/NB_QUEENS)
toolbox.register("select", tools.selTournament, tournsize=SELECTION_SIZE)

def main(seed=0):
    random.seed(seed)

    pop = toolbox.population(n=300)
    hof = tools.HallOfFame(5)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("Min", numpy.min)
    stats.register("Max", numpy.max)

    #cxpb – The probability of mating two individuals.
    #mutpb – The probability of mutating an individual.
    #ngen – The number of generation.
    algorithms.eaSimple(pop, toolbox, cxpb=MATING_PROB, mutpb=MUTATING_PROB, ngen=N_GENERATIONS, stats=stats,
                        halloffame=hof, verbose=True)

    return hof

if __name__ == "__main__":
    hall_of_fame = main()
    results = open('./nqueen_solutions/solutions.data', 'w')
    for r in hall_of_fame:
        results.write('{}\n'.format(r))
    results.close()