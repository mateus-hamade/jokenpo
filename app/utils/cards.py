import pygame

HEIGHT = 600
class Card(pygame.sprite.Sprite):
    def __init__(self, height, width, image):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(image)

        self.height = height
        self.width = width
        self.rect = self.image.get_rect()

        self.rect.center = (self.height, self.width)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.rect.y -= 5
            if self.rect.y < HEIGHT - 250:
                self.rect.y = HEIGHT - 250

        else:
            self.rect.y += 5
            if self.rect.y > HEIGHT - 100:
                self.rect.y = HEIGHT - 100

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            return True
        return False