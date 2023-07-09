import pygame
from copy import copy
from sudoku import Sudoku

pygame.init()

class Cell():
    def __init__(self, value, isClickable, fontColor):
        self.value = value
        self.isClickable = isClickable
        self.fontColor = fontColor
        self.notes = [0,0,0,0,0,0,0,0,0]

class Grid():
    def __init__(self):
        self.sudo = Sudoku()
        self.sudo.generate_grid()
        self.sudo.remove_nums(3)

        self.grid = [[Cell(self.sudo.grid[x][y],(self.sudo.grid[x][y] == 0),(128,128,128)) for y in range(9)] for x in range(9)] 
        self.lenX = len(self.sudo.grid)
        self.lenY = len(self.sudo.grid[0])
        self.sudo.solve_grid(self.sudo.grid)

        self.lastThreeStates = []
        self.chosenCell= []
        self.isNotesActivated = False
        
    def draw_grid(self):
        for i in range(10):
            #Set the thickness of the lines 
            if i % 3 == 0:
                thick = 4
            else:
                thick = 1
            #Draw the lines
            pygame.draw.line(screen, (0,0,0), (50, i*50+50), (500, i*50+50), thick)
            pygame.draw.line(screen, (0,0,0), (i * 50+50, 50), (i * 50+50, 500), thick)

        #Fill the grid with numbers
        for i in range(9):
            for j in range(9):
                if self.grid[i][j].value != 0:
                    value = (pygame.font.SysFont("kohinoorbangla", 40)).render(str(self.grid[i][j].value),1,self.grid[i][j].fontColor)
                    screen.blit(value,((j*50)+50+(50-value.get_width())//2,(i*50)+50+(50-value.get_height())//2))
                else:
                    if self.grid[i][j].notes:
                        for indx in range(len(self.grid[i][j].notes)):
                            if self.grid[i][j].notes[indx] != 0:
                                noteValue = (pygame.font.SysFont("kohinoorbangla", 10)).render(str(self.grid[i][j].notes[indx]),1,(128,128,128))
                                screen.blit(noteValue,((j*50)+50+((50//3)*(indx%3))+((50//3)-noteValue.get_width())//2,(i*50)+50+((50//3)*(indx//3))+((50//3)-noteValue.get_height())//2))
    
    def fill_in_cell(self, num):
        #Keep track of last three changes
        if len(self.lastThreeStates) >= 3:
            self.lastThreeStates.pop(0)
        self.lastThreeStates.append([self.chosenCell[0],self.chosenCell[1], self.grid[self.chosenCell[0]][self.chosenCell[1]].value, copy(self.grid[self.chosenCell[0]][self.chosenCell[1]].notes)])
        #Note down npossible cell values
        if self.isNotesActivated:
            if num > 0 and self.grid[self.chosenCell[0]][self.chosenCell[1]].value == 0:
                #Remove note value if it already exists
                if self.grid[self.chosenCell[0]][self.chosenCell[1]].notes[num-1]:
                    self.grid[self.chosenCell[0]][self.chosenCell[1]].notes[num-1] = 0
                else:
                    self.grid[self.chosenCell[0]][self.chosenCell[1]].notes[num-1] = num
        #Put down a value for the cell
        else:
            #Empty cell if the input value is same as previously inputted value
            if self.grid[self.chosenCell[0]][self.chosenCell[1]].value == num:
                self.grid[self.chosenCell[0]][self.chosenCell[1]].value = 0
            else:
                self.grid[self.chosenCell[0]][self.chosenCell[1]].value = num
                #Check if the input value is correct
                if self.sudo.solution[self.chosenCell[0]][self.chosenCell[1]] == num:
                    self.grid[self.chosenCell[0]][self.chosenCell[1]].fontColor = (70,130,180)
                else:
                    self.grid[self.chosenCell[0]][self.chosenCell[1]].fontColor = (220,20,60)

    #Choose a cell to enter input
    def is_cell_chosen(self, pos):
        x = (pos[0]//50)-1
        y = (pos[1]//50)-1
        if x < self.lenX and y < self.lenY and self.grid[y][x].isClickable:
            self.chosenCell = [y,x]
            return True
        return False
    
    #Update grid according to the clicked button
    def update_grid(self,button):
        if button[1] == 'reset':
            self.grid = [[Cell(self.sudo.grid[x][y],(self.sudo.grid[x][y] == 0),(128,128,128)) for y in range(9)] for x in range(9)] 
        elif button[1] == 'undo':
            if self.lastThreeStates:
                x,y,prevValue, prevNotes = self.lastThreeStates.pop()
                self.grid[x][y].value = prevValue
                self.grid[x][y].notes = prevNotes
        elif button[1] == 'solve':
            self.grid = [[Cell(self.sudo.solution[x][y],(self.sudo.grid[x][y] == 0),(128,128,128)) for y in range(9)] for x in range(9)] 
        else:
            button[0] = not button[0]
            self.isNotesActivated = button[0]

    #Choose a button to click on
    def click_on_button(self,mousePos,clickedButtons,isClicked):
        posX = 30
        for button in clickedButtons.keys():
            if (mousePos[0] >= posX and mousePos[0] <= posX+100 and mousePos[1] >= 550 and mousePos[1] <= 610):
                if isClicked:
                    self.update_grid(clickedButtons[button])
                color = (70,130,180)
            elif clickedButtons[button][0]:
                color = (70,130,180)
            else:
                color = (135,206,250)
            pygame.draw.rect(screen,(0,0,0),pygame.Rect(posX,550,100,60))
            pygame.draw.rect(screen,color,pygame.Rect(posX+5,555,90,50))
            screen.blit(button,(posX+20,565))
            posX+=130
 
def main():

    global screen, width, height
    g = Grid()

    width = 550
    height = 650
    icon = pygame.image.load("sudoku.png")
    pygame.display.set_icon(icon)

    screen = pygame.display.set_mode((width,height))
    pygame.display.set_caption("Sudoku")
    
    font = pygame.font.SysFont('Georgia',20,bold=True)
    undo = font.render('Undo',True, 'black')
    notes = font.render('Notes',True, 'black')
    reset = font.render('Reset',True, 'black')
    solve = font.render('Solve',True, 'black')
    clickedButtons = {undo: [False,'undo'], notes: [False,'notes'], reset: [False, 'reset'], solve: [False, 'solve']}

    running = True
    key = None
    
    while running:
        mousePos = pygame.mouse.get_pos()
        isClicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9

            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                clickedOnCell = g.is_cell_chosen(mousePos)
                isClicked = True
                if clickedOnCell:
                    key = -1          

        if g.chosenCell and key > 0:
            g.fill_in_cell(key)
            g.chosenCell = []
        
        screen.fill((255,255,255))
        g.click_on_button(mousePos,clickedButtons,isClicked)
        g.draw_grid()
        pygame.display.update()

main()


