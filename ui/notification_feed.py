import time
import pygame

class NotificationFeed:
    def __init__(self):
        self.x = 1200
        self.y = 50
        self.text = ""
        self.text_start = 0
        self.text_lifetime = 0

        self.font = pygame.font.SysFont(None, 20)

    def add_notification(self, text: str, lifetime: float):
        self.text = text
        self.text_start = time.time()
        self.text_lifetime = lifetime

    def update(self, screen):
        if not self.text:
            return

        elapsed = time.time() - self.text_start

        if elapsed > self.text_lifetime:
            self.text = ""
            self.text_start = 0
            self.text_lifetime = 0
            return

        self.render(screen, elapsed)

    def render(self, screen, elapsed):
        progress = elapsed / self.text_lifetime
        alpha = max(0, 255 * (1 - progress))

        text_surface = self.font.render(self.text, True, (255, 255, 255))

        text_surface = text_surface.convert_alpha()
        text_surface.set_alpha(int(alpha))

        text_rect = text_surface.get_rect()
        text_rect.topright = (self.x, self.y)

        screen.blit(text_surface, text_rect)