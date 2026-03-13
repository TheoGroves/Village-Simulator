from renderer import Renderer

class Villager:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.mood = "content"

    def render(self, renderer: Renderer):
        renderer.draw_circ(self.x, self.y, 1, (255, 255, 255))