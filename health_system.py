import random

class BodyPart:
    def __init__(self, name, health, part_type, affects, affect_amount=0):
        """Individual body part that affects high level stats"""
        self.name = name
        self.health = health
        self.MAX_HEALTH = health
        self.part_type = part_type # flesh, bone, organ
        self.affects = affects # what this body part affects when damaged
        self.affect_amount = affect_amount # how much the affected stats are changed by damage (0-1)

        self.injuries = [] # tuple(type, damage)

    def damage(self):
        POTENTIAL_INJURIES = []
        if self.part_type == "flesh":
            POTENTIAL_INJURIES = [("Cut", random.randint(1,3)), ("Laceration", random.randint(3,6))]
        elif self.part_type == "bone":
            POTENTIAL_INJURIES = [("Crack", random.randint(1,4)), ("Broken", random.randint(4,8))]
        elif self.part_type == "organ":
            POTENTIAL_INJURIES = [("Cut", random.randint(1,6)), ("Crush", random.randint(2,5))]
        self.injuries.append(random.choice(POTENTIAL_INJURIES))

    def update(self):
        self.health = self.MAX_HEALTH
        for injury in self.injuries:
            self.health -= injury[1] # reduce body part health by the damage of the injury

    def __repr__(self):
        return f"{self.name}: {self.health} - {self.injuries}"

class Affliction: 
    """Whole body injuries e.g. blood loss, malnutrition, illness, etc"""
    def __init__(self, name):
        self.name = name
        self.progress = 0
        self.progress_speed = 0

    def increase(self, speed):
        self.progress_speed += speed

    def set_rate(self, rate):
        self.progress_speed = rate

    def update(self):
        self.progress += self.progress_speed
        return self.progress >= 100

class HealthSystem:
    """High level health system that handles all body parts and afflictions"""
    def __init__(self):
        # Stats
        self.pain = 0
        self.consciousness = 100
        self.movement = 100
        self.manipulation = 100

        # Body
        self.body_parts = [
            BodyPart("Head", 20, "flesh", ["consciousness"], 0.3),
            BodyPart("Neck", 15, "flesh", []),
            BodyPart("Body", 40, "flesh", []),
            BodyPart("Left Arm", 20, "flesh", ["manipulation"], 0.5),
            BodyPart("Right Arm", 20, "flesh", ["manipulation"], 0.5),
            BodyPart("Left Leg", 25, "flesh", ["movement"], 0.5),
            BodyPart("Right Leg", 25, "flesh", ["movement"], 0.5)
        ]

        # Internal health
        self.blood_loss = Affliction("Blood Loss")
        self.malnutrition = Affliction("Malnutrition")

    def give_injury(self):
        part = random.choice(self.body_parts)
        part.damage()

    def update(self):
        self.blood_loss.update()
        self.malnutrition.update()

        self.pain = 0
        self.consciousness = 100
        self.movement = 100
        self.manipulation = 100

        for part in self.body_parts:
            part.update()
            health_proportion = part.health / part.MAX_HEALTH
            self.pain += ((1 - health_proportion) * part.affect_amount)
            stat_modifier = 1 - ((1 - health_proportion) * part.affect_amount)
            for affect in part.affects:
                if affect == "consciousness":
                    self.consciousness *= stat_modifier
                elif affect == "movement":
                    self.movement *= stat_modifier
                elif affect == "manipulation":
                    self.manipulation *= stat_modifier
                else:
                    print(f"Error: {part.name} affects {affect} which doesn't exist")
        print(f"Pain: {self.pain} | Consciousness: {self.consciousness} | Movement: {self.movement} | Manipulation: {self.manipulation}")