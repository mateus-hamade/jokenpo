import pygame
from pygame.locals import *

WIDTH = 480
HEIGHT = 185

class ImageAnimation(pygame.sprite.Sprite):

    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)        
        self.image_loading = pygame.image.load(image).convert()  
        self.image = self.image_loading     
        self.rect = self.image.get_rect()
        self.x = WIDTH 
        self.y = HEIGHT
        self.rect.center = (self.x, self.y)

        self.lifespan = 60
        self.speed = 1
        self.count = 0
        self.angle = 0


    def update(self):
        oldCenter = self.rect.center
        self.image = pygame.transform.rotate(self.image_loading, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = oldCenter

    def calcPos(self):
        self.x -= 5
        self.y = self.y

    def turnLeft(self):
        self.angle = (self.angle + 45) % 360

    def turnRight(self):
        self.angle = (self.angle - 45) % 360