import pygame

class PawnSelector:
    def __init__(self):
        self.selected_pawn = None

        self.font = pygame.font.SysFont(None, 20)
        self.top_left = (25, 500)
        self.padding = 10

        self.lines = 0
        self.scroll = 0

        self.panel_width = 450
        self.panel_height = 170

    def select_pawn(self, pawn):
        self.selected_pawn = pawn

    def handle_event(self, event):
        if event.type == pygame.MOUSEWHEEL:
            self.scroll -= event.y * 20
            self.scroll = max(0, self.scroll)

    def add_text(self, text, screen):
        text_surface = self.font.render(text, True, (255, 255, 255))

        y = self.top_left[1] + self.padding + self.lines * 20 - self.scroll

        text_rect = text_surface.get_rect(
            topleft=(self.top_left[0] + self.padding, y)
        )

        screen.blit(text_surface, text_rect)
        self.lines += 1

    def add_stat_bar(self, stat_name, stat_value, screen, bar_width=400, bar_height=20):
        y = self.top_left[1] + self.padding + self.lines * (bar_height + 10) - self.scroll
        bar_x = self.top_left[0] + self.padding

        # background
        pygame.draw.rect(screen, (40, 40, 40),
                         pygame.Rect(bar_x, y, bar_width, bar_height),
                         border_radius=5)

        # fill
        stat_bar_width = (stat_value / 100) * bar_width
        pygame.draw.rect(screen, (69, 98, 122),
                         pygame.Rect(bar_x, y, stat_bar_width, bar_height),
                         border_radius=5)

        # text
        stat_text = f"{stat_name}: {stat_value:.0f}%"
        text_surface = self.font.render(stat_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(
            center=(bar_x + bar_width / 2, y + bar_height / 2)
        )

        screen.blit(text_surface, text_rect)

        self.lines += 1

    def render(self, screen):
        if self.selected_pawn:
            panel_rect = pygame.Rect(
                self.top_left[0],
                self.top_left[1],
                self.panel_width,
                self.panel_height
            )

            pygame.draw.rect(screen, (80, 80, 80), panel_rect, border_radius=10)
            pygame.draw.rect(screen, (50, 50, 50), panel_rect, width=6, border_radius=10)

            screen.set_clip(panel_rect)

            self.lines = 0

            self.add_text(f"Name: {self.selected_pawn.name}", screen)
            self.add_text(f"Action: {self.selected_pawn.action}", screen)
            self.add_text("Stats:", screen)

            self.add_stat_bar("Food", self.selected_pawn.food, screen)
            self.add_stat_bar("Sleep", self.selected_pawn.sleep, screen)
            self.add_stat_bar("Recreation", self.selected_pawn.recreation, screen)

            screen.set_clip(None)