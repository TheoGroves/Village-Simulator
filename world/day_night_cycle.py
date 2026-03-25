import math

class DayNightCycle:
    def __init__(self, ticks_per_day):
        self.time = 0
        self.time_per_tick = 24 / ticks_per_day
        
        self.brightness = 0
    
    def update(self):
        self.time += self.time_per_tick
        self.brightness = (math.sin(math.radians(self.time * (360/24) - 90))+1) / 2