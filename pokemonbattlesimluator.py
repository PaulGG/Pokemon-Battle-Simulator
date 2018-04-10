from enum import Enum
import math
import random

class Nature(Enum):
    GOOD = 1.1
    NEUTRAL = 1.0
    BAD = 0.9

class Player: 
    def __init__(self, pokemon, backpack): 
        self.pokemon = pokemon 
        self.backpack = backpack 
 
class Pokemon:
    def __init__(self, name, hpStat, attackStat, defenseStat, spAttackStat, spDefenseStat, speedStat, level, moves, type1, type2, hpIV, 
        attackIV, defenseIV, spAttackIV, spDefenseIV, speedIV, hpEV, attackEV, defenseEV, spAttackEV, spDefenseEV, speedEV, nature, 
        growthRate, passive, healthStatus, itemHeld): 
        self.name = name
        # all stats must be betweeen 1 and 255
        self.hpStat = hpStat
        self.attackStat = attackStat
        self.defenseStat = defenseStat
        self.spAttackStat = spAttackStat
        self.spDefenseStat = spDefenseStat
        self.speedStat = speedStat
        # type
        self.type1 = type1
        self.type2 = type2


        # an IV must be between 0 and 31
        self.hpIV = hpIV
        self.attackIV = attackIV
        self.defenseIV = defenseIV
        self.spAttackIV = spAttackIV
        self.spDefenseIV = spDefenseIV
        self.speedIV = speedIV

        # an EV must be between 0 and 252
        self.hpEV = hpEV
        self.attackEV = attackEV
        self.defenseEV = defenseEV
        self.spAttackEV = spAttackEV
        self.spDefenseEV = spDefenseEV
        self.speedEV = speedEV

        # A pokemon's nature must be GOOD, NEUTRAL, or BAD
        self.nature = nature

        # A pokemon's growth rate (Level) is determined if it is Erratic, Fast, Medium Fast, Medium Slow, or Slow
        self.growthRate = growthRate
        self.xp = 0

        # Initial level for a pokemon
        self.level = level

        # passives are..a thing
        self.passive = passive

        # health status is like burn, paralyzed, etc.
        self.healthStatus = healthStatus

        # item held....has effects
        self.itemHeld = itemHeld

        # All of these are calculated with mathematical equations
        self.hp = ((2 * hpStat + hpIV + hpEV / 4 + 100) * level) / 100 + 10
        self.moves = moves
        self.attack = (((2 * attackStat + attackIV + attackEV / 4) * level) / 100 + 5) * nature
        self.spAttack = (((2 * spAttackStat + spAttackIV + spAttackEV / 4) * level) / 100 + 5) * nature
        self.defense = (((2 * defenseStat + defenseIV + defenseEV / 4) * level) / 100 + 5) * nature
        self.spDefense = (((2 * spDefenseStat + spDefenseIV + spDefenseEV / 4) * level) / 100 + 5) * nature
        self.speed = (((2 * speedStat + speedIV + speedEV / 4) * level) / 100 + 5) * nature

        def levelSetter(self, requiredXP):
            if self.xp >= requiredXP:
                    leftoverXP = self.xp - requiredXP
                    self.level += 1
                    xp = 0 + leftoverXP

        def erraticGrowth(self):
            if self.level >= 100:
                self.level = 100
                return
            if self.level < 50:
                requiredXP = (((level + 1) ** 3 * (100 - level + 1)) / 50) - (((level) ** 3 * (100 - level)) / 50)
                self.levelSetter(requiredXP)
            elif level >= 50 and level < 68:
                requiredXP = (((level + 1) ** 3 * (150 - level + 1)) / 100) - (((level) ** 3 * (150 - level)) / 100)
                self.levelSetter(requiredXP)
            elif level >= 68 and level < 98:
                requiredXP = (((level + 1) ** 3 * math.floor((1911 - (10 * level + 1)) / 3)) / 500) - (((level) ** 3 
                * math.floor((1911 - (10 * level)) / 3)) / 500)
                self.levelSetter(requiredXP)
            elif level >= 98 and level > 100:
                requiredXP = (((level + 1) ** 3 * (160 - level + 1)) / 100) - (((level) ** 3 * (160 - level)) / 100)
                self.levelSetter(requiredXP)
        
        def fastGrowth(self):
            if self.level >= 100:
                self.level = 100
            else:
                requiredXP = ((4 * (level + 1) ** 3) / 5) - ((4 * (level) ** 3) / 5)
                self.levelSetter(requiredXP)

        def mediumFastGrowth(self):
            if self.level >= 100:
                self.level = 100
            else:
                requiredXP = (level + 1) ** 3 - level ** 3
                self.levelSetter(requiredXP)
        
        def mediumSlowGrowth(self):
            if self.level >= 100:
                self.level = 100
            else:
                requiredXP = (((6 / 5) * (level + 1) ** 3) - (15 * (level + 1) ** 2) + 100 * (level + 1) - 140) -\
                (((6 / 5) * (level) ** 3) - (15 * (level) ** 2) + 100 * (level) - 140)
                self.levelSetter(requiredXP)
        
        def slowGrowth(self):
            if self.level >= 100:
                self.level = 100
            else:
                requiredXP = ((5 * (level + 1) ** 3) / 4) - ((5 * (level) ** 3) / 4) 
                self.levelSetter(requiredXP)
        
            
 
class Move: 
    def __init__(self, name, power, accuracy, damageType, type, pp):
        self.name = name
        self.power = power
        self.accuracy = accuracy
        self.damageType = damageType
        self.type = type
        self.pp = pp

    def determineWeatherMoveDamage(self):
        if self.type is "water" and environment.getWeather() is "raining":
            return 1.5
        elif self.type is "fire" and environment.getWeather() is "harsh_sunlight":
            return 1.5
        elif self.type is "water" and environment.getWeather() is "harsh_sunlight":
            return 0.5
        elif self.type is "fire" and environment.getWeather() is "raining":
            return 0.5
        else:
            return 1
    
    def determineCrit(self, attacker, defender):
        determiner = None
        if attacker.itemHeld in ["razor_claw", "scope_lens"] and attacker.passive is "super_luck" and self.name in ["slash, stone_edge"]:
            determiner = 0.333
        elif (attacker.itemHeld in ["razor_claw", "scope_lens"] and attacker.passive is "super_luck") or (attacker.itemHeld in ["razor_claw", 
            "scope_lens"] and self.name in ["slash, stone_edge"]) or (attacker.passive is "super_luck" and self.name in ["slash, stone_edge"]):
            determiner = 0.25
        elif attacker.itemHeld in ["razor_claw", "scope_lens"] or attacker.passive is "super_luck" or self.name in ["slash, stone_edge"]:
            determiner = 0.125
        else:
            determiner = 0.0625
        return 1.5 if random.random() <= determiner else 1

    def determineRandom(self, attacker, defender):
        i = random.random()
        while i < 0.85 or i > 1:
            i = random.random()
        return i
    

    def determineSTAB(self, attacker, defender):
        #TODO: possibly make passive into an objet
        if attacker.passive is "adaptability":
            return 2
        elif type is attacker.type1 or type is attacker.type2:
            return 1.5
        else:
            return 1

    def determineEffectiveness(self, attacker, defender):
        if defender.type1 or defender.type2 in self.type.typeEffective:
            if defender.type1 and defender.type2 in self.type.typeEffective:
                return 4
            else:
                return 2
        elif defender.type1 or defender.type2 in self.type.typeNotEffective:
            if defender.type1 and defender.type2 in self.type.typeNotEffective:
                return 0.25
            else:
                return 0.5
        elif defender.type1 or defender.type2 in self.type.typeImmunities:
            if defender.type2 is None and defender.type1 in self.type.typeImmunities:
                return 0
            elif defender.type1 is None and defender.type2 in self.type.typeImmunities:
                return 0
        else: return 1

    def determineBurn(self, attacker, defender):
        # TODO: healthStatus as object
        if attacker.healthStatus is "burned" and attacker.passive is not "guts" and self.damageType is "physical":
            return 0.5
        else: 
            return 1
    
    def damageFunc(self, attacker, defender):
        targets = 1
        weather = self.determineWeatherMoveDamage()
        critical = self.determineCrit(attacker, defender)
        rando = self.determineRandom(attacker, defender)
        STAB = self.determineSTAB(attacker, defender)
        effectiveness = self.determineEffectiveness(attacker, defender)
        burn = self.determineBurn(attacker, defender)
        # TODO: other is an item effect
        other = 1
        
        modifier = targets * weather * critical * rando * STAB * effectiveness * burn * other
        if self.damageType is "physical":
            return ((((2 * attacker.level) / 5 + 2) * self.power * (attacker.attack / defender.defense)) / 50 + 2) * modifier
        else: 
            return ((((2 * attacker.level) / 5 + 2) * self.power * (attacker.spAttack / defender.spDefense)) / 50 + 2) * modifier

    def use(self, attacker, defender):
            if self.pp <= 0:
                print("You don't have enough PP to use that move!")
            else:
                self.pp -= 1
                return self.damageFunc(attacker, defender)


class Environment:
    # All possible weather values are: Hail, Sandstorm, Rain, and Harsh Sunlight
    def __init__(self):
        self.value = "clear"
    
    def setRaining(self):
        value = "raining"
    
    def setHarshSunny(self):
        value = "harsh_sunlight"
    
    def setHailing(self):
        value = "hailing"
    
    def setSandstorm(self):
        value = "sandstorm"

    def getWeather(self):
        return self.value

class MoveSet:
    def __init__(self, move1, move2, move3, move4):
        self.move1 = move1
        self.move2 = move2
        self.move3 = move3
        self.move4 = move4

    def useMove1(self):
        return self.move1
    def useMove2(self):
        return self.move2
    def useMove3(self):
        return self.move3
    def useMove4(self):
        return self.move4

class Type: 
    def __init__(self, typeName): 
        self.typeName = typeName 
    
    def setEffectiveTypes(self, typeEffective):
        self.typeEffective = typeEffective
    
    def setNotEffectiveTypes(self, typeNotEffective):
        self.typeNotEffective = typeNotEffective
    
    def setImmuneTypes(self, typeImmunities):
        self.typeImmunities = typeImmunities
 
# Declaration of all pokemon types 
normal = Type("normal") 
fighting = Type("fighting")
flying = Type("flying")
poison = Type("poison")
ground = Type("ground")
rock = Type("rock")
bug = Type("bug")
ghost = Type("ghost")
steel = Type("steel")
fire = Type("fire")
water = Type("water")
grass = Type("grass")
electric = Type("electric")
psychic = Type("psychic")
ice = Type("ice")
dragon = Type("dragon")
dark = Type("dark")
fairy = Type("fairy")

# Helper function
def setTypes(type, effectiveTypes, notEffectiveTypes, immuneTypes):
    type.setEffectiveTypes(effectiveTypes)
    type.setNotEffectiveTypes(notEffectiveTypes)
    type.setImmuneTypes(immuneTypes)

# Setting type effectiveness
setTypes(fighting, [normal, rock, steel, ice, dark], [flying, poison, bug, psychic, fairy], ghost)
setTypes(flying, [fighting, bug, grass], [rock, steel, electric], None)
setTypes(poison, [grass, fairy], [poison, ground, rock, ghost], steel)
setTypes(ground, [poison, rock, steel, fire, electric], [bug, grass], flying)
setTypes(rock, [flying, bug, fire, ice], [fighting, ground, steel], None)
setTypes(bug, [grass, psychic, dark], [fighting, flying, poison, ghost, steel, fire, fairy], None)
setTypes(ghost, [ghost, psychic], [dark], normal)
setTypes(steel, [rock, ice, fairy], [steel, fire, water, electric], None)
setTypes(fire, [bug, steel, grass, ice], [rock, fire, water, dragon], None)
setTypes(water, [ground, rock, fire], [water, grass, dragon], None)
setTypes(grass, [ground, rock, water], [flying, poison, bug, steel, fire, grass, dragon], None)
setTypes(electric, [flying, water], [grass, electric, dragon], ground)
setTypes(psychic, [fighting, poison], [steel, psychic], dark)
setTypes(ice, [flying, ground, grass, dragon], [steel, fire, water, ice], dark)
setTypes(dragon, [dragon], [steel], fairy)
setTypes(dark, [ghost, psychic], [fighting, dark, fairy], None)
setTypes(fairy, [fighting, dragon, dark], [poison, steel, fire], None)

# list of all types 
types = [normal, fighting, flying, poison, ground, rock, bug, ghost, steel, fire, water, grass, electric, psychic, dragon, dark, fairy]

environment = Environment()


earthquake = Move("earthquake", 100, 100, "physical", ground, 10)
charizard = Pokemon("charizard", 78, 84, 78, 109, 85, 100, 50, MoveSet(Move("flamethrower", 90, 100, "special", fire, 15), Move("earthquake", 100, 100, 
"physical", ground, 10), Move("dragon_pulse", 85, 100, "special", dragon, 10), Move("rock_slide", 75, 90, "physical", rock, 10)), fire, flying, 31, 31, 
31, 31, 31, 31, 252, 252, 252, 252, 252, 252, 1.1, "medium_slow", "something", None, None)
venusaur = Pokemon("venusaur", 80, 82, 83, 100, 100, 80, 50, MoveSet(Move("solar_beam", 120, 100, "special", grass, 10), earthquake, Move("hidden_power", 
60, 100, "special", grass, 15), Move("energy_ball", 90, 100, "special", grass, 10)), grass, poison, 31, 31, 31, 31, 31, 31, 252, 252, 252, 252, 252, 252, 1.1, 
"medium_slow", "something", None, None)

print(str(charizard.moves.useMove1().use(charizard, venusaur)))