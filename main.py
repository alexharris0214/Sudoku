from curses import KEY_DOWN
from turtle import pen
from unicodedata import name
import pygame
pygame.init()

displayW = 800
displayH = 800
win = pygame.display.set_mode((displayW, displayH))
win.fill((255,255,255))
pygame.draw.line(win, (200,200,200), (50,50), (50,50), 2)

BLACK = (0,0,0)
RED = (255,0,0)

windowClock = pygame.time.Clock

class MainRun(object):
    ### Initialized Board object
    def __init__(self) -> None:
        self.dw = displayW
        self.dh = displayH
        self.currCell = (0,0)
        self.currentBoard = [[0,0,0,0,0,0,0,0,0], ### Board representation as a grid for solving purposes
                             [0,0,0,0,0,0,0,0,0],
                             [0,0,0,0,0,0,0,0,0],
                             [0,0,0,0,0,0,0,0,0],
                             [0,0,0,0,0,0,0,0,0],
                             [0,0,0,0,0,0,0,0,0],
                             [0,0,0,0,0,0,0,0,0],
                             [0,0,0,0,0,0,0,0,0],
                             [0,0,0,0,0,0,0,0,0],
                            ] 
        self.cells = {} ### Contains the cell rectanlge objects to be clickable and drawable

        ### Initalizing Rect Objects
        for i in range(9):
            for j in range(9):
                font = pygame.font.Font(None, 90)
                surface = font.render(" " + str(self.currentBoard[i][j]), True, (200,100,0))
                self.cells[(i,j)] = (pygame.Rect(60 + 75*j, 60 + 75*i, 75, 75), surface)
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

        for key, val in self.cells.items():
            rec = val[0]
            txt = val[1]
            win.blit(txt, (rec.x+5, rec.y+5))
            pygame.draw.rect(win, (255,100,25), rec, 1)

    def isClickedOn(self):
        pos = pygame.mouse.get_pos()
        for i in range(9):
            for j in range(9):
                rect = self.cells[(i,j)]
                if(rect[0].collidepoint(pos)):
                    return (list(rect),i,j)
        return None

    def main(self):
        run = True
        while(run):
            self.drawBoard()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    c = event.unicode
                    if((c == '1' or c == '2' or c == '3' or c == '4' or c == '5' or
                    c == '6' or c == '7' or c == '8' or c == '9') and self.currCell):
                        temp = list(self.cells[self.currCell])
                        font = pygame.font.Font(None, 90)
                        surface = font.render(" " + event.unicode, True, (200,100,0))
                        temp[1] = surface
                        self.cells[self.currCell] = tuple(temp)
                        self.currentBoard[self.currCell[0]][self.currCell[1]] = int(c)
                        self.currCell = None

                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    cell = self.isClickedOn()
                    tempRec = cell[0]
                    font = pygame.font.Font(None, 90)
                    surface = font.render(" " + str(self.currentBoard[cell[1]][cell[2]]), True, (200,0,0))
                    tempRec[1] = surface
                    self.cells[(cell[1],cell[2])] = tuple(tempRec)
                    self.currCell = (cell[1], cell[2])

                
if __name__ == "__main__":
    MainRun()