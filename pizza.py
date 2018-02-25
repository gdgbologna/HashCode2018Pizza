import numpy as np
import collections, math, itertools

filename = 'medium'

Point = collections.namedtuple('Point', ['x', 'y'])


def getArea(start: Point, end: Point):
    height = end.x - start.x + 1
    width = end.y - start.y + 1
    return height * width


def satifyMinIngredients(start: Point, end: Point):
    slice = pizza[start.x:(end.x + 1), start.y:(end.y + 1)]
    tomatoes = np.sum(slice)
    mushrooms = np.size(slice) - tomatoes

    if (tomatoes >= minIngredients) and (mushrooms >= minIngredients):
        return True
    else:
        return False


def checkOverlapping(start: Point, end: Point):
    pizzaSlice = pizza[start.x:(end.y + 1), start.y:(end.y + 1)]
    # if there's one or more cells with NaN value, the sum is NaN
    return math.isnan(pizzaSlice.sum())


def visitaCella(start: Point, end: Point):
    if end.x >= rows or end.y >= cols:
        return False, start, end, 0
    elif getArea(start, end) > maxCells or checkOverlapping(start, end):
        return False, start, end, 0
    elif satifyMinIngredients(start, end):
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


def cellVisit(firstCell: Point):
    slices = []
    counter = 0
    size = rows * cols
    cycled = itertools.cycle(np.ndenumerate(pizza))
    itertools.dropwhile(lambda index, x: (index[0] == firstCell.x) and (index[1] == firstCell.y), cycled)
    cell, value = next(cycled)
    while (counter <= size):
        while (math.isnan(value)):
            counter += 1
            cell, value = next(cycled)
        cell = Point(x=cell[0], y=cell[1])
        success, start, end, area = visitaCella(cell, cell)
        if (success):
            pizza[start.x:(end.x + 1), start.y:(end.y + 1)] = None
            slices.append({'start': start, 'end': end})
        cell, value = next(cycled)
        print(str(counter * 100 / size))
    solutions.append(slices)


def skipNan(index, x):
    return math.isnan(x)


def printSolution(solution):
    with open(filename + ".out", 'w+') as outputFile:
        outputFile.write('{}\n'.format(len(solution)))
        for slice in solution:
            start = slice['start']
            end = slice['end']
            outputFile.write('{} {} {} {}\n'.format(start.x, start.y, end.x, end.y))


with open(filename + ".in", 'r') as inputFile:
    # read file first line
    line = inputFile.readline()
    # parse parameter
    rows, cols, minIngredients, maxCells = [int(n) for n in line.split()]
    pizza = np.zeros([rows, cols])
    for row in range(rows):
        for ingredient, col in zip(inputFile.readline(), range(cols)):
            if ingredient == 'T':
                pizza[row, col] = 1
            else:
                pizza[row, col] = 0
    solutions = []
    cellVisit((0, 0))
    printSolution(solutions[0])
