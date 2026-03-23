class Item:
    def __init__(self, x, y, type, col):
        self.type = type 
        self.x = x
        self.y = y
        self.col = col

    def render(self, renderer):
        renderer.draw_circ(self.x, self.y, 0.7, self.col)

class ItemManager:
    def __init__(self):
        self.items = []

    def add_item(self, x, y, type, col):
        self.items.append(Item(x, y, type, col))

    def remove(self, item):
        if item in self.items:
            self.items.remove(item)

    def find_nearest_by_type(self, x, y, item_type):
        nearest_item = None
        nearest_distance = float("inf")

        for item in self.items:
            if item.type == item_type:
                distance = ((x - item.x) ** 2 + (y - item.y) ** 2)**0.5

                if distance < nearest_distance:
                    nearest_distance = distance
                    nearest_item = item

        return nearest_item
    
    def render(self, renderer):
        for item in self.items:
            item.render(renderer)