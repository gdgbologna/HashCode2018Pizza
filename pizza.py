import sys, os
import numpy as np
import collections, math, itertools

filename = 'small' if len(sys.argv) == 1 else sys.argv[1]

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

def visitaCella(start: Point, end: Point):
    if end.x >= rows or end.y >= cols:
        return False, start, end, 0
    elif getArea(start, end) > maxCells:
        return False, start, end, 0
    else:
        pizzaSlice = pizza[start.x:(end.x + 1), start.y:(end.y + 1)]
        sliceSum = np.sum(pizzaSlice)
        sliceSize = np.size(pizzaSlice)
        # if there's one or more cells with NaN value, the sum is NaN
        if math.isnan(sliceSum):
            return False, start, end, 0
        elif satifyMinIngredients(sliceSum,sliceSize):
            return True, start, end, getArea(start, end)
        else:
            # recursive case
            valid1, start1, end1, area1 = visitaCella(start, Point(x=end[0] + 1, y=end[1]))
            valid2, start2, end2, area2 = visitaCella(start, Point(x=end[0], y=end[1] + 1))
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


def trySlice(firstCell: Point,bestSolution):
    solution = {}
    solution['area'] = 0
    solution['slices'] = []
    counter = 0
    size = rows * cols
    cycled = itertools.cycle(np.ndenumerate(pizza))
    cell, value = next(cycled)
    while not ((cell[0] == firstCell.x) and (cell[1] == firstCell.y)):
        cell, value = next(cycled)
    while (counter <= size):
        while (math.isnan(value)):
            cell, value = next(cycled)
            counter += 1
        cell = Point(x=cell[0], y=cell[1])
        success, start, end, area = visitaCella(cell, cell)
        if (success):
            pizza[start.x:(end.x + 1), start.y:(end.y + 1)] = None
            solution['slices'].append({'start': start, 'end': end})
            solution['area']+=area
        cell, value = next(cycled)
        counter += 1
    if (solution['area']>=bestSolution['area']):
        bestSolution['area'] = solution['area']
        bestSolution['slices'] = solution['slices']


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
        # parse parameter
        global pizza, rows, cols, minIngredients, maxCells
        rows, cols, minIngredients, maxCells = [int(n) for n in line.split()]
        pizza = np.zeros([rows, cols])
        for row in range(rows):
            for ingredient, col in zip(inputFile.readline(), range(cols)):
                if ingredient == 'T':
                    pizza[row, col] = 1
                else:
                    pizza[row, col] = 0

inizializePizza()
bestSolution = {'area':0}
for index, value in np.ndenumerate(pizza):
    print(index)
    trySlice(Point(x=index[0], y=index[1]), bestSolution)
    inizializePizza()
    printSolution(bestSolution)
