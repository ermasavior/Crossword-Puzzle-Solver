'''
    TUGAS KECIL 1 STRATEGI ALGORITMA
    CROSSWORD PUZZLE SOLVER
    ERMA SAFIRA NURMASYITA
    13516072
    23 JANUARI 2018
'''
import sys
import operator
import time

### Data Structure ###
class Grid(object):
# Stores the properties of empty grids in the Puzzle
    def __init__(self, rowcol = (0, 0), length = 0, orient = None, prev = []):
        self.rowcol = rowcol # (row, column)
        self.length = length # empty grid length
        self.orient = orient # vertical or horizontal orientation
        self.prev = prev     # previous stored blocks before word placement

### Primitives ###
## Initialization ##
def FileToPuzzle(filename):
# Load puzzle from file
    global Puzzle, N, WordList
    file = open(filename, "r")
    filelist = file.read().splitlines()
    file.close()
    # number of board row and column
    N = int(filelist[0])
    # form puzzle board
    for i in range(1, N+1): 
        column = list(filelist[i])
        Puzzle.append(column)
    # list of words
    answer = filelist[N+1]
    WordList = answer.split(';')

def enumGrid(Puzzle, N):
# Enumerate the empty grids into GridList
    GridList = []
    j = 0
    gridlength = 0
    # Detecting blank grids horizontally
    for i in range(0 , N):   
        while (j < N):
            if Puzzle[i][j] == '-':
                while True:
                    gridlength += 1
                    j += 1
                    if (j >= N or Puzzle[i][j] == '#'):
                        if gridlength > 1:
                            rowcol = (i, j-gridlength)
                            GridList.append(Grid(rowcol, gridlength, 'hor', []))
                        break
                gridlength = 0
            else:
                j += 1
        j = 0
    # Detecting blank grids vertically
    i = 0
    gridlength = 0
    for j in range(0 , N):
        while (i < N):
            if Puzzle[i][j] == '-':
                while True:
                    gridlength += 1
                    i += 1
                    if (i >= N or Puzzle[i][j] == '#'):
                        if gridlength > 1:
                            rowcol = (i-gridlength, j)
                            GridList.append(Grid(rowcol, gridlength, 'ver', []))
                        break
                gridlength = 0
            else:
                i += 1
        i = 0
    GridList.sort(key=operator.attrgetter('rowcol')) # sort grids based on row & column tuple
    return GridList

def initPuzzle(filename):
# Load puzzle from file and enumerate grids which can be filled out
    global Puzzle, N, GridList, WordList, UsedWordList   
    Puzzle = []
    WordList = []
    FileToPuzzle(filename)
    GridList = enumGrid(Puzzle, N)
    UsedWordList = [False]*len(WordList) # Save each word's usage status

## Crossword Solver ##
def GridToWord(grid):
# Transform Grid in Puzzle board into list of char
    row = grid.rowcol[0]
    col = grid.rowcol[1]
    Word = []
    if grid.orient == 'hor':
        for i in range (0, grid.length):
            Word.append(Puzzle[row][col+i])
    else:
        for i in range (0, grid.length):
            Word.append(Puzzle[row+i][col])
    return Word

def isWordFit(Grid, Word):
# Check whether a Word fits to an unsolved grid
# Precond: len(Word) and Grid.length is not zero
    if Grid.length == len(Word):
        i = 0
        isFit = True
        GridWord = GridToWord(Grid)
        while isFit and i < Grid.length:
            if GridWord[i] != '-' and GridWord[i] != Word[i]:
                isFit = False
            else:
                i += 1
        return isFit
    else:
        return False     

def WriteWordinGrid(Word, Grid):
# Write a Word to the Grid in puzzle board
# Precond: Word is fit for Grid
    global Puzzle
    row = Grid.rowcol[0]
    col = Grid.rowcol[1]
    j = 0
    (Grid.prev) = []
    if (Grid.orient == 'hor'):
        for i in range(0, Grid.length):
            (Grid.prev).append(Puzzle[row][col+i])
            Puzzle[row][col+i] = Word[j]
            j += 1
    else:
        for i in range(0, Grid.length):
            (Grid.prev).append(Puzzle[row+i][col])            
            Puzzle[row+i][col] = Word[j]
            j += 1

def PuzzleSolver(idxGrid):
# Solve Puzzle with brute force algorithm with recursive approach
    global GridList, UsedWordList, issolved, stop_time
    if (idxGrid == len(GridList)):  # Basis: All grids are solved
        stop_time = time.time()
        issolved = True
        printPuzzle(Puzzle)
    else:
        for idxWord in range(0, len(WordList)):
            Grid, Word = GridList[idxGrid], WordList[idxWord]
            if (not UsedWordList[idxWord] and isWordFit(Grid, Word)):
                # Write Word to Grid with index idxGrid
                WriteWordinGrid(Word, Grid)
                UsedWordList[idxWord] = True
                if not issolved:
                    # Recurrence
                    PuzzleSolver(idxGrid + 1)
                # Clear Word from Grid with index idxGrid
                WriteWordinGrid(Grid.prev, Grid)
                UsedWordList[idxWord] = False

def solvePuzzle():
# Procedure for puzzle solver; print and timer
    global issolved, time
    issolved = False    # Puzzle board solved-status
    start_time = time.time()
    PuzzleSolver(0)     # Algorithm to solve
    time = stop_time - start_time

## Output ##
def printPuzzle(PuzzleBoard):
# Print Crossword Puzzle
    i, j = 0, 0
    for i in range(0, N):
        for j in range(0, N):
            print("%c " % PuzzleBoard[i][j], end="")
        print()

### Main Program ###
initPuzzle(sys.argv[1])   # sys.argv[1] = filename
print("-- CROSSWORD PUZZLE SOLVER --")
solvePuzzle()   # Solve, print, and count time execution for solving puzzle
print("*** Crossword Puzzle has been solved for %s sec(s) ***" % (time))


'''
When in Doubt (Just In Case)
def SearchWord(WordList, Grid):
# Traverse all words and return if it fits the grid 
    i = 0
    isFound = False
    while ((not isFound) and i < len(WordList)):
        if isWordFit(Grid, WordList[i]):
            isFound = True
        else:
            i += 1
    if isFound:
        return i
    else:
        return -1

def PuzzleSolver(WordList):
# Crossword puzzle solver with Brute Force method
    global Puzzle, N, GridList, UsedWordList
    i = 0
    while i < len(GridList):    ### Under Construction
        printPuzzle(Puzzle)
        idxWord = SearchWord(WordList, GridList[i])
        if idxWord != -1:
            if not UsedWordList[idxWord]:
                GridList[i].prev = GridToWord(GridList[i])
                WriteWordinGrid(WordList[idxWord], GridList[i])
                UsedWordList[idxWord] = True
                i += 1
            else:
                i -= 1
                UsedWordList[idxWord] = False
        else:
            i -= 1
            GridWord = ''.join(GridToWord(GridList[i]))
            WriteWordinGrid(GridList[i].prev, GridList[i])

'''