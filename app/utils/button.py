from subprocess import check_call
import pygame
from pygame.locals import *

class Button():
    def __init__(self, text, image, width, height, pos, elevation):
        # Core attributes
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]
        self.image = image

        # load image background
        if self.image != None:
            self.image = pygame.image.load(image)

        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = '#403C60'

        # bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = '#1D1B2B'
        
        # text
        self.text_surf = pygame.font.Font('assets/fonts/Quicksand-Bold.ttf', 26).render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self, screen):
        if self.image != None:
            screen.blit(self.image, (900, 15))

            self.check_click()
        else:
            # elevation logic   
            self.top_rect.y = self.original_y_pos - self.dynamic_elecation
            self.text_rect.center = self.top_rect.center

            self.bottom_rect.midtop = self.top_rect.midtop
            self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

            pygame.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius=8)
            pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=8)
            screen.blit(self.text_surf, self.text_rect)

            self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#659AFF'
            if pygame.mouse.get_pressed()[0]:                
                self.dynamic_elecation = 0
                self.pressed = True
                return True
            else:
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    self.pressed = False
                    return False
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = '#403C60'