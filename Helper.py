from cmath import rect
from typing import List
from xmlrpc.client import Boolean
import pygame

def checkCollision(pos,  rect: pygame.rect.Rect) -> Boolean:
    return rect.collidepoint(pos)

def isValid(grid: List[List[int]]) -> Boolean:
    for row in range(len(grid)):
        for col in range(len(grid)):
            # check value is an int
            if grid[row][col] < 1 or type(grid[row][col]) is not type(1):
                return False
            # check value is within 1 through n.
            # for example a 2x2 grid should not have the value 8 in it
            elif grid[row][col] > len(grid):
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
