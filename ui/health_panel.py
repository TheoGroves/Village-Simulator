import pygame
from helpers import mouse_in_rect

class HealthPanel:
    def __init__(self):
        self.selected_pawn = None

        self.font = pygame.font.SysFont(None, 20)
        self.top_left = (25, 180)
        self.padding = 10

        self.lines = 0
        self.scroll = 0

        self.panel_width = 450
        self.panel_height = 300

    def select_pawn(self, pawn):
        self.selected_pawn = pawn

    def handle_event(self, event):
        if event.type == pygame.MOUSEWHEEL and mouse_in_rect(pygame.Rect(self.top_left[0], self.top_left[1], self.panel_width, self.panel_height)):
            self.scroll -= event.y * 20
            self.scroll = max(0, self.scroll)

    def add_text(self, text, screen, color=(255,255,255)):
        text_surface = self.font.render(text, True, color)

        y = self.top_left[1] + self.padding + self.lines * 20 - self.scroll

        screen.blit(text_surface, (self.top_left[0] + self.padding, y))
        self.lines += 1

    def add_bar(self, name, value, screen, max_value=100, color=(150,50,50)):
        bar_width = 400
        bar_height = 18

        y = self.top_left[1] + self.padding + self.lines * (bar_height + 6) - self.scroll
        x = self.top_left[0] + self.padding

        # background
        pygame.draw.rect(screen, (40,40,40), (x, y, bar_width, bar_height), border_radius=4)

        # fill
        fill = max(0, min(1, value / max_value))
        pygame.draw.rect(screen, color, (x, y, bar_width * fill, bar_height), border_radius=4)

        # text
        txt = f"{name}: {value:.0f}"
        text_surface = self.font.render(txt, True, (255,255,255))
        screen.blit(text_surface, (x + 5, y))

        self.lines += 1

    def render(self, screen):
        if not self.selected_pawn:
            return

        health = self.selected_pawn.health

        panel_rect = pygame.Rect(
            self.top_left[0],
            self.top_left[1],
            self.panel_width,
            self.panel_height
        )

        pygame.draw.rect(screen, (80,80,80), panel_rect, border_radius=10)
        pygame.draw.rect(screen, (50,50,50), panel_rect, 6, border_radius=10)

        screen.set_clip(panel_rect)

        self.lines = 0

        self.add_text("Health", screen)

        if health.dead:
            self.add_text("DEAD", screen, (255, 50, 50))
        elif health.unconscious:
            self.add_text("UNCONSCIOUS", screen, (255, 200, 50))

        self.add_bar("Pain", health.pain * 100, screen)
        self.add_bar("Consciousness", health.consciousness, screen)
        self.add_bar("Movement", health.movement, screen)
        self.add_bar("Manipulation", health.manipulation, screen)

        self.add_bar("Blood Loss", health.blood_loss.progress, screen)
        self.add_bar("Malnutrition", health.malnutrition.progress, screen)

        self.add_text(" ", screen)
        self.add_text(" ", screen)

        self.add_text("Body Parts:", screen)

        for part in health.body_parts:
            health_ratio = part.health / part.MAX_HEALTH
            if health_ratio < 0.3:
                color = (255, 80, 80)
            elif health_ratio < 0.7:
                color = (255, 180, 80)
            else:
                color = (200, 200, 200)

            self.add_text(f"{part.name} ({part.health}/{part.MAX_HEALTH})", screen, color)

            if part.bleeding > 0:
                self.add_text(f"  Bleeding: {part.bleeding}", screen, (255,100,100))

            for injury in part.injuries:
                self.add_text(f"  - {injury[0]} ({injury[1]})", screen, (180,180,180))

        screen.set_clip(None)