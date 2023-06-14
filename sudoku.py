import math
from enum import Enum
import copy

class BoxDraw(Enum):
    H_LINE = "─"
    V_LINE = "│"
    CORNER_UP_LEFT = "┌"
    CORNER_UP_RIGHT =  "┐"
    JUNCTION_LEFT = "├"
    JUNCTION_RIGHT = "┤"
    JUNCTION_ALL = "┼"

# test1 was the tricky one we tried in the pub
test1 = [
    [1,0,0,3,0,0,2,0,0],
    [0,0,0,6,5,7,0,4,0],
    [7,0,5,1,0,0,0,0,0],
    [0,0,2,0,7,0,0,0,3],
    [5,0,0,0,0,0,0,0,4],
    [0,3,8,0,6,0,0,0,1],
    [0,0,0,0,0,0,0,0,0],
    [0,9,0,0,0,2,8,7,0],
    [3,0,0,0,0,1,0,0,0]
]

test2 = [
    [0,0,6,0,1,0,0,0,0],
    [0,5,0,4,0,0,7,0,0],
    [0,0,0,0,0,0,8,2,5],
    [5,0,0,7,0,0,0,0,0],
    [0,9,0,0,3,0,0,0,0],
    [3,4,0,0,0,0,0,5,9],
    [0,0,1,0,0,2,0,7,8],
    [9,0,0,0,6,3,0,0,0],
    [0,0,0,0,0,0,6,0,0]
]

invalidTest1 = [
    [1,0,0,3,0,0,2,0,0],
    [0,1,0,6,5,7,0,4,0],
    [7,0,5,1,0,0,0,0,0],
    [0,0,2,0,7,0,0,0,3],
    [5,0,0,0,0,0,0,0,4],
    [0,3,8,0,6,0,0,0,1],
    [0,0,0,0,0,0,0,0,0],
    [0,9,0,0,0,2,8,7,0],
    [3,0,0,0,0,1,0,0,0]
]

def printPuzzle(puzzle):
    print ("┌───┬───┬───┐")
    r = 1
    for row in puzzle:
        print ("│", end="") 
        c = 0
        for n in row:
            if n != 0:
                print (n, end="")
            else:
                print (" ", end="")
            if c == 2:
                print ("│",end="")
                c = 0
            else:
                c+=1
        print ("\n", end="")
        if r == 3 or r == 6:
            print ("├───┼───┼───┤")
        elif r == 9:
            print ("└───┴───┴───┘")
        r += 1

# box should be a 2D array with 3 elements, each with 3 elemnts
def printBox(box):
    print ("┌───┐")
    for row in box:
        print ("│", end="")
        for i in range(0,3):
            n = row[i]
            if (n != 0):
                print (n, end="")
            else:
                print (" ", end="")
        print ("│\n", end="")
    print ("└───┘")

# Gets box n from a puzzle. For example, for test 1, that would be cells (0,0) to [2,2]
def getBox(puzzle, n):
    startX = ((n-1) % 3) * 3
    startY = math.floor((n-1) / 3) * 3
    row1 = row2 = row3 = []
    x = 1
    for i in range(startY, startY + 3):
        row = []
        for j in range(startX, startX + 3):
            row.append(puzzle[i][j])
        if (x == 1):
            row1 = row
        elif (x == 2):
            row2 = row
        else:
            row3 = row
        x+=1
    return [row1, row2, row3]

def getRow(puzzle, n):
    row = []
    for i in range(0, 9):
        row.append(puzzle[n][i])
    return row

def getColumn(puzzle, n):
    column = []
    for i in range(0, 9):
        column.append(puzzle[i][n])
    return column

def isValid(puzzle):
    # Do the horizontals
    for row in puzzle:
        seen = []
        for number in row:
            if number in seen and number != 0:
                # print ("Failed on horizontals")
                # print ("Horizontal: " + str(number))
                return False
            else:
                seen.append(number)
    # Do the verticals
    for i in range (0, 9):
        seen = []
        for j in range (0,9):
            number = puzzle[j][i]
            if number in seen and number != 0:
                # print ("Failed on vertcials")
                # print ("Vertical: " + str(number))
                return False
            else:
                seen.append(number)
    # Do the boxes
    for i in range(1, 10):
        box = getBox(puzzle, i)
        seen = []
        for row in box:
            for number in row:
                if number in seen and number != 0:
                    # print ("Failed on boxes")
                    # print ("Box: " + str(i) + ". Number: " + str(number))
                    return False
                else:
                    seen.append(number)
    return True

# the puzzle passed here should ALWAYS be valid
def crosses(puzzle, n):
    # printPuzzle (puzzle)
    if n == 0:
        print ("That's a 0. You can't do that!")
        return 0
    # Start by checking rows
    for row in puzzle:
        for number in row:
            if number == n:
                # replace all spaces with Xs
                for i in range (0,9):
                    if row[i] == 0:
                        row[i] = "X"
    for c in range(0,9):
        for r in range(0,9):
            number = puzzle[r][c]
            if number == n:
                # replace all spaces with Xs
                for i in range (0,9):
                    if puzzle[i][c] == 0:
                        puzzle[i][c] = "X"
    # boxes!
    for i in range(1, 10):
        startX = ((i-1) % 3) * 3
        startY = math.floor((i-1) / 3) * 3
        for x in range(startY, startY + 3):
            for y in range(startX, startX + 3):
                number = puzzle[x][y]
                if number == n:
                    for x2 in range(startY, startY + 3):
                        for y2 in range(startX, startX + 3):
                            if puzzle[x2][y2] == 0:
                                puzzle[x2][y2] = "X"
    return puzzle

# given a crossResult produced by the crosses function, this function will see if there are any places...
# ... where n can go. If so, it will provide the coordinates in an array
def findSpotInCrossResult(crossResult):
    # printPuzzle (crossResult)
    marks = []
    # check row
    for r in range (0, 9):
        row = getRow(crossResult, r)
        if row.count(0) == 1:
            c = row.index(0)
            marks.append(tuple([r, c]))
            # print ("row added " + str(r) + " " + str(c))
    # check column
    for c in range (0, 9):
        column = getColumn(crossResult, c)
        if column.count(0) == 1:
            r = column.index(0)
            marks.append(tuple([r, c]))
            # print ("column added " + str(r) + " " + str(c))
    # check box
    for i in range (1,10):
        box = getBox(crossResult, i)
        spaceCount = 0
        for x in range (0, 3):
            for y in range(0, 3):
                if box[x][y] == 0:
                    spaceCount+=1
        if spaceCount == 1:
            for x in range (0,3):
                for y in range(0,3):
                    if box[x][y] == 0:
                        startX = ((i-1) % 3) * 3
                        startY = math.floor((i-1) / 3) * 3
                        c = startX + y
                        r = startY + x
                        marks.append(tuple([r,c]))
                        # print ("box added " + str(r) + " " + str(c))
    marks = list(dict.fromkeys(marks)) # Make list unique
    return marks
def checkAndMark(puzzleToCheck):
    newPuzzle = copy.deepcopy(puzzleToCheck)
    for n in range (1, 10):
        crossResultToMark = crosses(copy.deepcopy(puzzleToCheck), n)
        marks = findSpotInCrossResult(crossResultToMark)
        for mark in marks:
            r, c = mark
            newPuzzle[r][c] = n
        # print (n, marks)
    return newPuzzle

def startBacktracing(puzzle):
    for a in range(0,9):
        for b in range(0,9):
            number = puzzle[a][b]
            if number == 0:
                return backtracing(puzzle, a, b)

# x and y are the location of the number to change
def backtracing(puzzle, x, y):
    printPuzzle(puzzle)
    newPuzzle = copy.deepcopy(puzzle)
    while (newPuzzle[x][y] < 9):
        print (x, y )
        newPuzzle[x][y] += 1
        if isValid(newPuzzle) == True:
            # find the next open space
            x+=1
            if x == 9:
                y += 1
                x = 0
            while True:
                if y >= 9:
                    # we've found it
                    return puzzle
                if newPuzzle[x][y] == 0:
                    break
                else:
                    x+=1
                    if x == 9:
                        y += 1
                        x = 0
            result = backtracing(copy.deepcopy(newPuzzle), x, y)
            if result != False:
                return result
    return False    

def solve(puzzle):
    print ("Before logic:")
    printPuzzle(puzzle)
    # bf = before, af = after
    bf = puzzle
    af = checkAndMark(bf)
    # logic!
    while bf != af:
        bf = af
        af = checkAndMark(bf)
    print ("After logic: ")
    printPuzzle(af)
    completed = startBacktracing(af)
    print (completed)
    printPuzzle(completed)

# printPuzzle(crosses(test1, 6))
# printPuzzle(crosses(test1,6))
solve(test1 )