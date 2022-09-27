from curses import KEY_DOWN
import re
from turtle import pen
from unicodedata import name
import pygame

from Helper import checkCollision, isValid
pygame.init()

displayW = 1000
displayH = 800
win = pygame.display.set_mode((displayW, displayH))
win.fill((255,255,255))
pygame.draw.line(win, (200,200,200), (50,50), (50,50), 2)

BLACK = (0,0,0)
RED = (255,0,0)

clock = pygame.time.Clock()

class MainRun(object):
    ### Initialized Board object
    def __init__(self) -> None:
        self.dw = displayW
        self.dh = displayH
        self.currCell = None
        self.currentBoard = [[0,6,0,3,0,0,8,0,4], ### Board representation as a grid for solving purposes
                             [5,3,7,0,9,0,0,0,0],
                             [0,0,0,0,0,6,3,0,7],
                             [0,9,0,0,5,1,2,3,8],
                             [0,0,0,0,0,0,0,0,0],
                             [7,1,3,6,2,0,0,4,0],
                             [3,0,6,4,0,0,0,1,0],
                             [0,0,0,0,6,0,5,2,3],
                             [1,0,2,0,0,9,0,8,0],
                            ]
        self.setCells = [(0,1),(0,3),(0,6),(0,6),(0,8),
            (1,0),(1,1),(1,2),(1,4),
            (2,5),(2,6),(2,8),
            (3,1),(3,4),(3,5),(3,6),(3,7),(3,8),
            (5,0),(5,1),(5,2),(5,3),(5,4),(5,7),
            (6,0),(6,2),(6,3),(6,7),
            (7,4),(7,6),(7,7),(7,8),
            (8,0),(8,2),(8,5),(8,7)
        ]
        self.cells = {} ### Contains the cell rectanlge objects to be clickable and drawable
        self.buttons = self.populateButtons()
        ### Initalizing Rect Objects
        for i in range(9):
            for j in range(9):
                self.cells[(i,j)] = pygame.rect.Rect(65 + 75*j, 65 + 75*i, 70, 70)
        self.main()

    def drawBoard(self) -> None:
        penColor = BLACK
        win.fill((255,255,255))
        for i in range(10):
            if(i % 3 == 0):
                penColor = RED
            pygame.draw.line(win, penColor, (60 + 75 * i,60), (60 + 75 * i, 735), 2)
            penColor = BLACK
        for i in range(10):
            if(i % 3 == 0):
                penColor = RED
            pygame.draw.line(win, penColor, (60,60 + 75 * i), (735, 60 + 75 * i), 2)
            penColor = BLACK

        ### Populating grid objects
        for i in range(9):
            for j in range(9):
                rec = self.cells[(i,j)]
                font = pygame.font.Font(None, 90)
                if(self.currentBoard[i][j] == 0): 
                    surface = font.render(" ", True, (200,100,0))
                else:
                    if((i,j) in self.setCells): 
                        surface = font.render(" " + str(self.currentBoard[i][j]), True, (0,0,0))
                    else:
                        surface = font.render(" " + str(self.currentBoard[i][j]), True, (255,100,0))
                win.blit(surface, (rec.x+5, rec.y+5))
                if((i,j) == self.currCell):
                    pygame.draw.rect(win, (0,255,0), rec, 2) ## IF there is a rect selected, color it green
                else:
                    pygame.draw.rect(win, (255,255,255), rec, 1) ## Make non- selected rects transparent

        for button in self.buttons:
            win.blit(button[1], (button[0].x + 10, button[0].y + 10))
            pygame.draw.rect(win, (0,0,0), button[0], 5)

    def getSelectedCell(self):
        pos = pygame.mouse.get_pos()
        for i in range(9):
            for j in range(9):
                rect = self.cells[(i,j)]
                if(checkCollision(pos, rect)):
                    return (rect,i,j)
        return None

    def getSelectedButton(self):
        pos = pygame.mouse.get_pos()
        for b in self.buttons:
            if(b[0].collidepoint(pos)):
                return b[0]
        return None

    def handleButton(self, button: pygame.rect.Rect):
        match(button.y):
            case(100):
                if(isValid(self.currentBoard)):
                    print("You won")
                else:
                    print("Not a valid puzzle")

    
    def populateButtons(self):
        validate = pygame.rect.Rect(800, 100, 110, 50)
        solve = pygame.rect.Rect(800, 200, 110, 50)
        reset = pygame.rect.Rect(800, 300, 110, 50)

        font = pygame.font.Font(None, 45)

        validateSurface = font.render("Check", True, (255,0,255))
        solveSurface = font.render("Solve", True, (255,0,255))
        resetSurface = font.render("Reset", True, (255,0,255))

        return [(validate, validateSurface), (solve, solveSurface), (reset, resetSurface)]

    def main(self):
        run = True
        while(run):
            clock.tick(60)
            self.drawBoard()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    c = event.unicode
                    ### If the key pressed is a digit and there is currently a cell selected
                    if((c == '1' or c == '2' or c == '3' or c == '4' or c == '5' or
                    c == '6' or c == '7' or c == '8' or c == '9' or c == '0') and self.currCell):
                        self.currentBoard[self.currCell[0]][self.currCell[1]] = int(c) # Updating the value in the board
                        self.currCell = None # Reseting currCell to be non selected after a cell was changed
                elif event.type == pygame.MOUSEBUTTONUP:
                    cell = self.getSelectedCell()
                    if(cell):
                        i = cell[1]
                        j = cell[2]
                        if((i,j) not in self.setCells):
                            self.currCell = (cell[1], cell[2])
                    button = self.getSelectedButton()
                    if(button):
                        self.handleButton(button)

if __name__ == "__main__":
    MainRun()