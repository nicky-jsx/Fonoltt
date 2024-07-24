import pygame
from utils import COLOURS

class Button:
    def __init__(self, text, x, y, width, height, color=COLOURS['BLACK'], text_color=COLOURS['WHITE']):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font = pygame.font.Font(None, 32)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, COLOURS['WHITE'], self.rect, 2)  # Change border color to white
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class TextInput:
    def __init__(self, x, y, width, height, font_size=32):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = COLOURS['WHITE']
        self.text = ""
        self.font = pygame.font.Font(None, font_size)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode


    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, COLOURS['BLACK'], self.rect, 2)
        text_surface = self.font.render(self.text, True, COLOURS['BLACK'])
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

class ProgressBar:
    def __init__(self, x, y, width, height, max_value):
        self.rect = pygame.Rect(x, y, width, height)
        self.max_value = max_value
        self.current_value = 0

    def update(self, value):
        self.current_value = min(value, self.max_value)

    def draw(self, screen):
        pygame.draw.rect(screen, COLOURS['BLACK'], self.rect, 2)
        fill_width = int((self.current_value / self.max_value) * self.rect.width)
        fill_rect = pygame.Rect(self.rect.left, self.rect.top, fill_width, self.rect.height)
        pygame.draw.rect(screen, COLOURS['GREEN'], fill_rect)

def position_text(text, font, max_width):
        lines = []
        for line in text.split('\n'):
            words = line.split()
            current_line = []
            for word in words:
                test_line = current_line + [word]
                if font.size(' '.join(test_line))[0] <= max_width:
                    current_line.append(word)
                else:
                    lines.append(' '.join(current_line))
                    current_line = [word]
            lines.append(' '.join(current_line))
        return lines
