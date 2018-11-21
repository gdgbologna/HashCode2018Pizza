import sys, os
import numpy as np
import collections, math, random
import itertools
import multiprocessing

# if not input file specified use first one
filename = 'small' if len(sys.argv) == 1 else sys.argv[1]

lock = multiprocessing.Lock()

Point = collections.namedtuple('Point', ['x', 'y'])

def getArea(start: Point, end: Point):
    height = end.x - start.x + 1
    width = end.y - start.y + 1
    return height * width


def satifyMinIngredients(pizzaSliceSum,sliceSize):
    tomatoes = pizzaSliceSum
    mushrooms = sliceSize - tomatoes
    if (tomatoes >= minIngredients) and (mushrooms >= minIngredients):
        return True
    else:
        return False

def visitaCella(start: Point, end: Point, mypizza):
    # if the slice exceeded pizza size
    if end.x >= rows or end.y >= cols:
        return False, start, end, 0
    # if the slice size exceeded max slice size
    elif getArea(start, end) > maxCells:
        return False, start, end, 0
    else:
        # evalueate pizze splice
        pizzaSlice = mypizza[start.x:(end.x + 1), start.y:(end.y + 1)]
        sliceSum = np.sum(pizzaSlice)
        sliceSize = np.size(pizzaSlice)
        # if there's one or more cells with NaN value, the sum is NaN
        if math.isnan(sliceSum):
            return False, start, end, 0
        elif satifyMinIngredients(sliceSum,sliceSize):
            return True, start, end, getArea(start, end)
        else:
            # recursive case
            # expand on the right
            valid1, start1, end1, area1 = visitaCella(start, Point(x=end[0] + 1, y=end[1]), mypizza)
            # expand on the bottom
            valid2, start2, end2, area2 = visitaCella(start, Point(x=end[0], y=end[1] + 1), mypizza)
            # if both valid
            if valid1 and valid2:
                # return minimum size
                if (area1 <= area2):
                    return True, start1, end1, area1
                else:
                    return True, start2, end2, area2
            elif valid1:
                return True, start1, end1, area1
            elif valid2:
                return True, start2, end2, area2
            else:
                return False, start, end, 0


def trySlice(pointList, mypizza):
    solution = {}
    solution['area'] = 0
    solution['slices'] = []
    # for each cell
    for cell,value in pointList:
            if (not math.isnan(value)):
                cell = Point(x=cell[0], y=cell[1])
                success, start, end, area = visitaCella(cell, cell, mypizza)
                if (success):
                    mypizza[start.x:(end.x + 1), start.y:(end.y + 1)] = None
                    solution['slices'].append({'start': start, 'end': end})
                    solution['area']+=area
    with bestSolution.get_lock():
        if (solution['area']>bestSolution.value):
            bestSolution.value = solution['area']
            printSolution(solution)


def skipNan(index, x):
    return math.isnan(x)


def printSolution(solution):
    outfilepath = "out/" + filename + ".out"
    os.makedirs(os.path.dirname(outfilepath), exist_ok=True)
    with open(outfilepath, 'w+') as outputFile:
        outputFile.write('{}\n'.format(len(solution['slices'])))
        for slice in solution['slices']:
            start = slice['start']
            end = slice['end']
            outputFile.write('{} {} {} {}\n'.format(start.x, start.y, end.x, end.y))

def inizializePizza():
    with open("in/" + filename + ".in", 'r') as inputFile:
        # read file first line
        line = inputFile.readline()
        # parse parameters
        rows, cols, minIngredients, maxCells = [int(n) for n in line.split()]
        # crate an array representing pizza
        # 1 are tomatoes and 10 are mushrooms
        pizza = np.zeros([rows, cols])
        for row in range(rows):
            for ingredient, col in zip(inputFile.readline(), range(cols)):
                if ingredient == 'T':
                    pizza[row, col] = 1
                else:
                    pizza[row, col] = 0
        return pizza, rows, cols, minIngredients, maxCells

def printEx(ex):
    print(ex)

import time
now = time.time()
pizza, rows, cols, minIngredients, maxCells = inizializePizza()
print("time to initialize pizza = "+str(now-time.time()))
all_cells = list(np.ndenumerate(pizza))
num_permutation = math.factorial(len(all_cells))
permutations = list()
global bestSolution
bestSolution = multiprocessing.Value('i',0)
import sys
i=0
pool = multiprocessing.Pool()
for permutation in itertools.permutations(all_cells):
    percent = (i*100)/num_permutation
    with bestSolution.get_lock():
        sys.stdout.write("\r{}% BestArea = {}".format(percent,bestSolution.value))
    sys.stdout.flush()
    #pizza_copy = pizza.copy()
    #trySlice(permutations,pizza_copy)
    pool.apply_async(trySlice,args=[permutation,pizza],error_callback=printEx)
    i=i+1
pool.join()
