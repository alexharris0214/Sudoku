from pygame import init


class Solver():
    def isPuzzleValid(self, grid: list[list[int]]) -> bool:
        for row in range(len(grid)):
            for col in range(len(grid)):
                # check value is an int
                if (grid[row][col] < 1 or type(grid[row][col]) is not type(1)) or (grid[row][col] > len(grid)):
                    return False
        # check the rows
        for row in grid:
            if sorted(list(set(row))) != sorted(row):
                return False
        # check the cols
        cols = []
        for col in range(len(grid)):
            for row in grid:

                cols += [row[col]]
            # set will get unique values, its converted to list so you can compare
            # it's sorted so the comparison is done correctly.
            if sorted(list(set(cols))) != sorted(cols):
                return False
            cols = []
        # if you get past all the false checks return True
        return True
    
    def isCellValid(self, board, num, row, col):
        for i in range(len(board[0])):
            if(board[row][i] == num and col != i):
                return False
        for i in range(len(board)):
            if(board[i][col] == num and row != i):
                return False
        xBox = col // 3
        yBox = row // 3
        for i in range(yBox * 3, yBox * 3 + 3):
            for j in range(xBox * 3, xBox * 3 + 3):
                if board[i][j] == num and i != row and j != col:
                    return False
        return True


    def findEmpty(self, board)-> tuple[int,int]:
        for row in range(len(board)):
            for col in range(len(board[row])):
                if(board[row][col] == 0):
                    return (row,col)
