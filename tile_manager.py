from perlin_noise import perlin_octaves

class TileType:
    def __init__(self, selected):
        self.potentials = ["Water", "Grass", "Dirt", "Rock", "Wall", "Plant"]
        self.set_type(selected)

    def get_type(self) -> str:
        return self.selected

    def set_type(self, selected):
        if isinstance(selected, int):
            self.selected = self.potentials[selected]
        elif isinstance(selected, str) and selected in self.potentials:
            self.selected = self.potentials[self.potentials.index(selected)]
        else:
            self.selected = "None"

class Tile:
    def __init__(self, type: TileType):
        self.tile_type = type.get_type()
        self.colour = self.determine_colour(self.tile_type)
        self.height = 0

    def set_type(self, type:str):
        tile = TileType("")
        tile.set_type(type)
        self.tile_type = tile.get_type()
        self.colour = self.determine_colour(self.tile_type)

    def set_height(self, height):
        self.height = height
        remapped = 0.3*self.height + 0.7
        self.height_colour = (self.colour[0]*remapped, self.colour[1]*remapped, self.colour[2]*remapped)


    def render(self, x, y, renderer):
        # special tiles
        if self.tile_type == "Plant":
            renderer.draw_rect(x, y, 1, 1, (194, 237, 119))
            renderer.draw_circ(x, y, 1, self.height_colour)
        # default tiles
        else:
            renderer.draw_rect(x, y, 1, 1, self.height_colour)
    
    @staticmethod
    def determine_colour(tile_type: str):
        if tile_type == "Water":
            colour = (186, 238, 247) # blue
        elif tile_type == "Grass":
            colour = (194, 237, 119) # light green
        elif tile_type == "Dirt":
            colour = (74, 63, 55) # brown
        elif tile_type == "Rock":
            colour = (59, 59, 59) # dark grey        
        elif tile_type == "Wall":
            colour = (150, 150, 150) # light grey
        elif tile_type == "Plant":
            colour = (81, 156, 16) # dark green
        else: # missing tile type
            colour = (255, 0, 255) # magenta
        return colour

class TileManager:
    def __init__(self, width, height, octaves=8):
        import time
        self.tiles = [[Tile(TileType("")) for x in range(width)] for y in range(height)]

        gen_start = time.time()
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[0])):
                height = perlin_octaves(x*0.05,y*0.05,0, octaves)
                from smoothstep import smoothstep_n
                smoothstepped = smoothstep_n(height, 10)
                self.tiles[y][x].set_type(self.determine_type(smoothstepped))
                self.tiles[y][x].set_height(smoothstepped)
        print(f"Generate world of size {len(self.tiles[0])}x{len(self.tiles)} in {(time.time()-gen_start):.2f} seconds")
    
    def determine_type(self, height):
        if height > 0.8:
            return "Rock"
        if height > 0.4:
            return "Grass"
        if height > 0.2:
            return "Dirt"
        return "Water"
    
    def render(self, renderer):
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[0])):
                self.tiles[y][x].render(x,y,renderer)