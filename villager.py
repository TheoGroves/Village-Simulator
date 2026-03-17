from renderer import Renderer

class Villager:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.mood = "content"

    def follow_path(self, path):
        if not path == []:
            self.x = path[0][0]
            self.y = path[0][1]
            path.pop(0)

    def render(self, renderer: Renderer):
        renderer.draw_circ(self.x, self.y, 1, (255, 255, 255))