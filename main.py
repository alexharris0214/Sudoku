import time
import pygame
from Helper import checkCollision
from PuzzleLoader import Loader
from Solver import Solver
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
        self.filePath = './puzzles.json'
        self.puzzleLoader = Loader(self.filePath)
        if(not self.puzzleLoader.tryFile()):
            quit()
        self.solver = Solver()
        self.dw = displayW
        self.dh = displayH
        self.currCell = None
        self.currentBoard = self.puzzleLoader.loadBoard('easy')
        self.setCells = [(0,1),(0,3),(0,6),(0,6),(0,8),
                         (1,0),(1,1),(1,2),(1,4),
                         (2,5),(2,6),(2,8),
                         (3,1),(3,4),(3,5),(3,6),(3,7),(3,8),
                         (5,0),(5,1),(5,2),(5,3),(5,4),(5,7),
                         (6,0),(6,2),(6,3),(6,7),
                         (7,4),(7,6),(7,7),(7,8),
                         (8,0),(8,2),(8,5),(8,7)
                        ]
        self.cells = {} ### Contains the cell rectangle objects to be clickable and drawable
        self.buttons = self.populateButtons()
        self.labels = {
            "win" : pygame.rect.Rect(770, 400, 200, 60),
            "lose" : pygame.rect.Rect(770, 400, 210, 50)
        }
        self.labelsToDraw = []
        ### Initializing Rect Objects
        for i in range(9):
            for j in range(9):
                self.cells[(i,j)] = pygame.rect.Rect(63 + 75*j, 63 + 75*i, 72, 72)
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
                win.blit(surface, (rec.x, rec.y+5))
                if((i,j) == self.currCell):
                    pygame.draw.rect(win, (0,255,0), rec, 2) ## IF there is a rect selected, color it green
                else:
                    pygame.draw.rect(win, (255,255,255), rec, 1) ## Make non- selected rects transparent

        # Prints the buttons on screen
        for button in self.buttons:
            win.blit(button[1], (button[0].x + 10, button[0].y + 10))
            pygame.draw.rect(win, (0,0,0), button[0], 5)

        # Prints the labels on screen, where desciptor is the description of the label
        # where label is the rect object itself for the label
        for descriptor, label in self.labels.items():
            if(descriptor in self.labelsToDraw):
                if(descriptor == 'win'):
                    font = pygame.font.Font(None, 60)
                    surface = font.render("You win!", True, (0,0,0))
                    win.blit(surface, (label.x + 10, label.y+10))
                    pygame.draw.rect(win, (255,100,100), label, 2)
                elif(descriptor == 'lose'):
                    font = pygame.font.Font(None, 40)
                    surface = font.render("Puzzle Invalid", True, (0,0,0))
                    win.blit(surface, (label.x + 10, label.y+10))
                    pygame.draw.rect(win, (255,100,100), label, 2)
                
    # Attempts to find the current Sudoku cell that is selected
    # If none found, return none
    def getSelectedCell(self) -> tuple[pygame.rect.Rect, int, int]:
        pos = pygame.mouse.get_pos()
        for i in range(9):
            for j in range(9):
                rect = self.cells[(i,j)]
                if(checkCollision(pos, rect)):
                    return (rect,i,j)
        return None

    # Find the current button pressed if it is, returns None if not
    def getSelectedButton(self) -> pygame.rect.Rect:
        pos = pygame.mouse.get_pos()
        for b in self.buttons:
            if(b[0].collidepoint(pos)):
                return b[0]
        return None

    #Handles the pressed button according;y
    def handleButton(self, button: pygame.rect.Rect) -> bool:
        case = button.y
        #Check Button
        if(case == 100):
            if(self.solver.isPuzzleValid(self.currentBoard)):
                self.labelsToDraw.append("win")
                try:
                    self.labelsToDraw.remove("lose")
                except ValueError:
                    pass
            else:
                self.labelsToDraw.append("lose")
                try:
                    self.labelsToDraw.remove("win")
                except ValueError:
                    pass
        # Solve button
        elif(case == 200):
            self.solve()
        # Reset button
        elif(case == 300):
            self.__init__()

    def solve(self):
        clock.tick(50)
        find = self.solver.findEmpty(self.currentBoard)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1,10):
            if(self.solver.isCellValid(self.currentBoard, i, row, col)):
                self.currentBoard[row][col] = i
                self.drawBoard()
                pygame.display.update()
                if(self.solve()):
                    
                    return True
                self.currentBoard[row][col] = 0
                self.drawBoard()
                pygame.display.update()
        return False


    #Creates rectangle objects for buttons
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
                        self.currCell = None # Reset currCell to be non selected after a cell was changed
                elif event.type == pygame.MOUSEBUTTONUP:
                    cell = self.getSelectedCell()
                    if(cell): # Clicked rectangle was a Sudoku cell
                        i = cell[1]
                        j = cell[2]
                        if((i,j) not in self.setCells):
                            self.currCell = (cell[1], cell[2])
                        self.labelsToDraw = []
                    else:
                        button = self.getSelectedButton()
                        if(button): # Clicked rectangle was a button
                            self.handleButton(button)

if __name__ == "__main__":
    MainRun()