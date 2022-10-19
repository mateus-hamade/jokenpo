import pygame
from pygame.locals import *

class Image:
    def __init__(self, image, x, y, width, height):
        self.image = pygame.image.load(image)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def draw(self, screen):        
        screen.blit(self.image, (self.x, self.y))