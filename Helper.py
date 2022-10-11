import pygame

def checkCollision(pos,  rect: pygame.rect.Rect) -> bool:
    return rect.collidepoint(pos)