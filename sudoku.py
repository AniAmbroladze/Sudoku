
from random import shuffle
from copy import deepcopy


class Sudoku():
    def __init__(self):
        self.grid = [[0 for x in range(9)] for y in range(9)] 
        self.lenX = len(self.grid)
        self.lenY = len(self.grid[0])
        self.numList = [1,2,3,4,5,6,7,8,9]
        self.count = 0
        self.solution = []

    def print_board(self):
        for x in range(0,self.lenX):
            if x%3 == 0 and x != 0:
                print("- - - - - - - - - - - - - - - - -")
            for y in range(0,self.lenY):
                if y%3 == 0 and y != 0:
                    print(" | ", end ="")
                if y == 8:
                    print(" " +str(self.grid[x][y])+ " ")
                else:
                    print(" "+str(self.grid[x][y])+" ", end="")

    def check_possibility(self,currentGrid,num, x, y):
        #Check if there are duplicates in a row
        for y1 in range(self.lenY):
            if currentGrid[x][y1] == num and y1 != y:
                return False
        #Check if there are duplicates in a column
        for x1 in range(self.lenX):
            if currentGrid[x1][y] == num and x1 !=x:
                return False
        #Check if there are duplicates in a 3x3 square
        square_x = x//3*3
        square_y = y//3*3
        for x1 in range(square_x, square_x+3):
            for y1 in range(square_y,square_y+3):
                if currentGrid[x1][y1] == num and x1 != x and y1 != y:
                    return False
        return True
    
    def check_vailidty(self,currentGrid):
        for x in range(self.lenX):
            for y in range(self.lenY):
                if currentGrid[x][y]!=0 and self.check_possibility(currentGrid,currentGrid[x][y],x,y) == False:
                    return False
        return True

    def solve_grid(self,currentGrid):
        for x in range(self.lenX):
            for y in range(self.lenY):
                #Find zeros (empty cells) in the grid
                if currentGrid[x][y] == 0:
                    #Check which number could be a fit
                    for i in range(1,10):
                        if self.check_possibility(currentGrid,i,x,y):
                            currentGrid[x][y] = i
                            #Check for the rest of the empty cells
                            if self.solve_grid(currentGrid):
                                self.solution = deepcopy(currentGrid)
                                self.count+=1
                            currentGrid[x][y] =  0
                    return False
        return True

    def generate_grid(self):
        for x in range(self.lenX):
            for y in range(self.lenY):
                #Find zeros (empty cells) in the grid
                if self.grid[x][y] == 0:
                    #Put random number in the cell
                    shuffle(self.numList)
                    for num in self.numList:
                        #Check the validity of the chosen random number
                        if self.check_possibility(self.grid,num,x,y):
                            self.grid[x][y] = num
                            #Fill in the rest of the empty cells
                            if self.generate_grid():
                                return self.grid
                            self.grid[x][y] = 0
                    return False
        return True

    def remove_nums(self,diff):
        while diff > 0:
            xNumList = [0,1,2,3,4,5,6,7,8]
            yNumList = [0,1,2,3,4,5,6,7,8]
            shuffle(xNumList)
            shuffle(yNumList)      
            for x in xNumList:
                for y in yNumList:
                    buff = self.grid[x][y]
                    if buff !=0:
                        self.grid[x][y] = 0
                        currentGrid = deepcopy(self.grid)
                        self.solve_grid(currentGrid)
                        if self.count > 1:
                            self.grid[x][y] = buff
                        else:
                            diff-=1
                        self.count = 0







