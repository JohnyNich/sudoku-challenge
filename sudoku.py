import math
from enum import Enum

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

def isValid(puzzle):
    # Do the horizontals
    for row in puzzle:
        seen = []
        for number in row:
            if number in seen and number != 0:
                print ("Failed on horizontals")
                print ("Horizontal: " + str(number))
                return False
            else:
                seen.append(number)
    # Do the verticals
    for i in range (0, 9):
        seen = []
        for j in range (0,9):
            number = puzzle[j][i]
            if number in seen and number != 0:
                print ("Failed on vertcials")
                print ("Vertical: " + str(number))
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
                    print ("Failed on boxes")
                    print ("Box: " + str(i) + ". Number: " + str(number))
                    return False
                else:
                    seen.append(number)
    return True

print (isValid(invalidTest1))