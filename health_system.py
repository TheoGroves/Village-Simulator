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

        self.bleeding = 0 # How much the injury bleeds
        self.injuries = [] # tuple(type, damage)

    def damage(self):
        # injury(name, damage, bleedrate)
        CUT = ("Cut", random.randint(1,3), random.randint(1,4))
        LACERATION = ("Laceration", random.randint(3,6), random.randint(5,9))
        CRACK = ("Crack", random.randint(1,4), 0)
        BROKEN = ("Broken", random.randint(4,8), 0)
        CRUSH = ("Crush", random.randint(2,5), random.randint(1,2))

        POTENTIAL_INJURIES = []
        if self.part_type == "flesh":
            POTENTIAL_INJURIES = [CUT, LACERATION]
        elif self.part_type == "bone":
            POTENTIAL_INJURIES = [CRACK, BROKEN]
        elif self.part_type == "organ":
            POTENTIAL_INJURIES = [CUT, CRUSH]
        self.injuries.append(random.choice(POTENTIAL_INJURIES))

    def update(self):
        self.health = self.MAX_HEALTH
        self.bleeding = 0
        for injury in self.injuries:
            self.bleeding += injury[2] # increase body part bleeding by the bleedrate of the injury
            self.health -= injury[1] # reduce body part health by the damage of the injury
        self.health = max(0, self.health)

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
        self.progress = max(0, min(self.progress, 100))
        return self.progress > 99

    def __repr__(self):
        return f"{self.name}: {self.progress:.0f}/100"

class HealthSystem:
    """High level health system that handles all body parts and afflictions"""
    def __init__(self):
        self.dead = False
        self.unconscious = False

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
        self.NECCESSARY_BODY_PARTS = [
            "Head",
            "Neck",
            "Body"
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

        bleeding = 0

        for part in self.body_parts:
            part.update()
            health_proportion = part.health / part.MAX_HEALTH
            if health_proportion == 0 and part.name in self.NECCESSARY_BODY_PARTS:
                self.dead = True
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

            bleeding += part.bleeding
        self.blood_loss.set_rate((bleeding ** 1.2) / 75)

        # affect stats
        self.consciousness *= (1 - (self.blood_loss.progress / 100) * 0.7)
        self.consciousness *= max(0, 1 - self.pain * 0.3)
        self.movement *= (self.consciousness/100)
        self.manipulation *= (self.consciousness/100)

        self.unconscious = self.consciousness < 20 or self.pain > 0.6

        if self.blood_loss.progress > 99 or self.malnutrition.progress > 99 or self.consciousness < 1:
            self.dead = True
                
        print(f"Pain: {self.pain:.2f} | Consciousness: {self.consciousness:.0f} | Movement: {self.movement:.0f} | Manipulation: {self.manipulation:.0f} | Afflictions: {self.blood_loss}, {self.malnutrition}")