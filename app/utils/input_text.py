import pygame
import time

class InputText:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color('#403C60')
        self.text = text
        self.txt_surface = pygame.font.Font('assets/fonts/Quicksand-Bold.ttf', 26).render(text, True, self.color)
        self.active = False
        self.text_return = ''

        self.cursor = pygame.Rect(0, 0, 2, 20)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False

            self.color = pygame.Color('#403C60') if self.active else pygame.Color('#000552')
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    self.text_return = self.text
                    self.text = self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

                self.txt_surface = pygame.font.Font('assets/fonts/Quicksand-Bold.ttf', 26).render(self.text, True, self.color)

    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        if self.active:
            pygame.draw.rect(screen, self.color, self.rect, 3, border_radius=7)
        else:
            pygame.draw.rect(screen, self.color, self.rect, 2, border_radius=7)

        if self.active:
            if time.time() % 1 > 0.5:
                text_rect = self.txt_surface.get_rect(topleft = (self.rect.x + 7, self.rect.y + 10))
                self.cursor.midleft = text_rect.midright

                pygame.draw.rect(screen, self.color, self.cursor)

    def return_text(self):
        if self.text_return != '':
            return self.text_return