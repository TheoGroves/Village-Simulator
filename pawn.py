from renderer import Renderer
from tile_manager import ROCK, WATER
from health_system import HealthSystem
import random
import pygame

TONES = [
    (255, 244, 219),
    (230, 215, 184),
    (209, 189, 146),
    (99, 84, 51),
    (54, 45, 25)
]

MALE_NAMES = [
    "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph",
    "Charles", "Thomas", "Christopher", "Daniel", "Matthew", "Anthony", "Donald", "Mark",
    "Paul", "Steven", "Andrew", "Joshua", "Kenneth", "Kevin", "Brian", "George", 
    "Timothy", "Ronald", "Jason", "Jeffrey", "Ryan", "Jacob", "Gary", "Nicholas",
    "Eric", "Stephen", "Larry", "Justin", "Benjamin", "Samuel", "Adam", "Gregory",
    "Harry", "Frank", "Raymond", "Jack", "Alexander", "Henry", "Douglas", "Joe",
    "Zachary", "Peter", "Walter", "Christian", "Austin", "Kyle", "Ethan", "Jacob",
    "Craig", "Leo", "Wayne", "Austin"
]

FEMALE_NAMES = [
    "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica",
    "Sarah", "Karen", "Nancy", "Betty", "Helen", "Dorothy", "Sandra", "Ashley",
    "Kimberly", "Emily", "Donna", "Michelle", "Carol", "Amanda", "Melissa", "Deborah",
    "Rebecca", "Laura", "Sharon", "Cynthia", "Kathleen", "Amy", "Shirley", "Anna",
    "Ruth", "Debra", "Virginia", "Kathryn", "Maria", "Frances", "Carolyn", "Christine",
    "Rachel", "Janet", "Emma", "Catherine", "Diane", "Teresa", "Janice", "Julia",
    "Grace", "Beverly", "Hannah", "Mildred", "Theresa", "Betty", "Joan", "Evelyn",
    "Alice", "Judy", "Cheryl", "Hannah", "Joan", "Diana", "Brittany", "Madeline"
]

class Pawn:
    def __init__(self, x, y, tile_manager):
        # engine
        self.x = x
        self.y = y
        self.tone = random.choice(TONES)
        self.gender = random.choice(["Male", "Female"])
        self.name = ""
        if self.gender == "Male":
            self.name = random.choice(MALE_NAMES)
        else:
            self.name = random.choice(FEMALE_NAMES)
        self.drafted = False
        self.sleeping = False

        # pathfinding
        self.tile_manager = tile_manager
        self.last_target = (0,0)
        self.path = []

        # scheduler
        self.action = ""
        self.queue = []

        # health
        self.health = HealthSystem()

        # stats (0-100)
        self.food = 100
        self.sleep = 100
        self.recreation = 100

    def determine_action(self, plant_manager, item_manager):
        # Priorities:

        # Get Food
        if self.food <= 30: # Try eat when hungry
            food = item_manager.find_nearest_by_type(self.x, self.y, "Food")
            if food: # If food exists, eat it else continue through priorities
                if not self.path: # If not moving, pathfind towards food
                    self.action = "Finding Food"
                    self.pathfind(food.x, food.y)
                
                if self.x == food.x and self.y == food.y: # Eat when standing on food
                    item_manager.remove(food)
                    self.food = 100

        # Sleep
        if self.sleep == 0: # Pass out from exaughstion
            self.sleeping = True

        # Get Recreation - TODO
        # Work
        plant = plant_manager.find_nearest_mature_plant(self.x, self.y)
        if plant: # If a mature plant exists, work else wander
            if not self.path: # If not moving, pathfind towards plant
                self.action = "Harvesting"
                self.pathfind(plant.x, plant.y)

            if self.x == plant.x and self.y == plant.y: # Harvest when standing on plant
                plant.harvest(item_manager)
            return

        # Wander
        if not self.path:
            self.action = "Wandering"
            self.pathfind(self.x + random.randint(-20, 20), self.y + random.randint(-20, 20))

    def update(self, renderer, plant_manager, item_manager):
        if not self.sleeping: # While awake:
            if self.drafted: # Manual pathfinding when drafted
                self.drafted_pathfind(renderer)
            else: # Automatic AI pathfinding when undrafted
                self.determine_action(plant_manager, item_manager)

            if self.path: # Follow path automatically if one exists
                self.follow_path(self.path)
        else:
            self.action = "Sleeping"
            self.sleep += 1
            if self.sleep > 99:
                self.sleeping = False
        
        # Update health
        if self.food < 1:
            self.health.malnutrition.set_rate(0.5)
        self.health.update()

        # Decay stats
        self.food -= 0.125
        self.sleep -= 0.125
        self.recreation -= 0.125

        self.food = max(0, min(100, self.food))
        self.sleep = max(0, min(100, self.sleep))
        self.recreation = max(0, min(100, self.recreation))

    def pathfind(self, x, y):
        self.path = self.tile_manager.find_path(self.x, self.y, x, y)
    
    def drafted_pathfind(self, renderer):
        path = []
        mouse_x = int((pygame.mouse.get_pos()[0]+renderer.x)/renderer.grid_size)
        mouse_y = int((pygame.mouse.get_pos()[1]+renderer.y)/renderer.grid_size)
        if (mouse_x, mouse_y) != self.last_target and self.drafted:
            if pygame.mouse.get_pressed()[0]:
                path = self.tile_manager.find_path(self.x, self.y, mouse_x, mouse_y)
                self.last_target = (mouse_x, mouse_y)
        if path:
            self.path = path

    def follow_path(self, path):
        if not path == []:
            self.x = path[0][0]
            self.y = path[0][1]
            path.pop(0)

    def set_random_pos(self, tile_manager):
        """Sets a random pos, avoiding impassable terrain - use for spawning villagers"""
        test_x = random.randint(0, tile_manager.width-1)
        test_y = random.randint(0, tile_manager.height-1)
        type = tile_manager.tiles[test_y][test_x].type
        while type == ROCK or type == WATER:
            test_x = random.randint(0, tile_manager.width-1)
            test_y = random.randint(0, tile_manager.height-1)
            type = tile_manager.tiles[test_y][test_x].type
        self.x = test_x
        self.y = test_y

    def damage(self):
        self.health.give_injury()
        print(self.health.body_parts)

    def render(self, renderer: Renderer):
        renderer.draw_circ(self.x, self.y, 1.3, (0,0,0))
        renderer.draw_circ(self.x, self.y, 1, self.tone)

        if self.path:
            for x,y in self.path:
                renderer.draw_circ(x, y, 0.5, (255, 255, 255))