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
    def __init__(self, hpStat, attackStat, defenseStat, spAttackStat, spDefenseStat, speedStat, hp, xp, level, moves, attack, spAttack, defense, spDefense, speed, type1, type2, hpIV, attackIV, defenseIV, spAttackIV, spDefenseIV, speedIV
        , hpEV, attackEV, defenseEV, spAttackEV, spDefenseEV, speedEV, nature, growthRate): 
        # all stats must be betweeen 1 and 255
        self.hpStat = hpStat
        self.attackStat = attackStat
        self.defenseStat = defenseStat
        self.spAttackStat = spAttackStat
        self.spDefenseStat = spDefenseStat
        self.speedStat = speedStat

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
        self.xp = xp

        # Initial level for a pokemon
        self.level = level
        # All of these are calculated with mathematical equations
        self.hp = ((2 * hpStat + hpIV + hpEV / 4 + 100) * level) / 100 + 10
        self.moves = moves
        self.attack = (((2 * attackStat + attackIV + attackEV / 4) * level) / 100 + 5) * nature
        self.spAttack = (((2 * spAttackStat + spAttackIV + spAttackEV / 4) * level) / 100 + 5) * nature
        self.defense = (((2 * defenseStat + defenseIV + defenseEV / 4) * level) / 100 + 5) * nature
        self.spDefense = (((2 * spDefenseStat + spDefenseIV + spDefenseEV / 4) * level) / 100 + 5) * nature
        self.speed = (((2 * speedStat + speedIV + speedEV / 4) * level) / 100 + 5) * nature

        def levelSetter(self, requiredXP):
            if xp >= requiredXP:
                    leftoverXP = xp - requiredXP
                    level++
                    xp = 0 + leftoverXP

        def erraticGrowth(self):
            if level >= 100:
                level = 100
                return
            if level < 50:
                requiredXP = (((level + 1) ** 3 * (100 - level + 1)) / 50) - (((level) ** 3 * (100 - level)) / 50)
                levelSetter(requiredXP)
            elif level >= 50 and level < 68:
                requiredXP = (((level + 1) ** 3 * (150 - level + 1)) / 100) - (((level) ** 3 * (150 - level)) / 100)
                levelSetter(requiredXP)
            elif level >= 68 and level < 98:
                requiredXP = (((level + 1) ** 3 * math.floor((1911 - (10 * level + 1)) / 3)) / 500) - (((level) ** 3 * math.floor((1911 - (10 * level)) / 3)) / 500)
                levelSetter(requiredXP)
            elif level >= 98 and level > 100:
                requiredXP = (((level + 1) ** 3 * (160 - level + 1)) / 100) - (((level) ** 3 * (160 - level)) / 100)
                levelSetter(requiredXP)
        
        def fastGrowth(self):
            if level >= 100:
                level = 100
            else:
                requiredXP = ((4 * (level + 1) ** 3) / 5) - ((4 * (level) ** 3) / 5)
                levelSetter(requiredXP)

        def mediumFastGrowth(self):
            if level >= 100:
                level = 100
            else:
                requiredXP = (level + 1) ** 3 - level ** 3
                levelSetter(requiredXP)
        
        def mediumSlowGrowth(self):
            if level >= 100:
                level = 100
            else:
                requiredXP = (((6 / 5) * (n + 1) ** 3) - 15 * ((n + 1)) ** 2) + (100 * (n + 1)) - 140) - (((6 / 5) * (n) ** 3) - 15 * ((n)) ** 2) + (100 * (n)) - 140)
                levelSetter(requiredXP)
        
        def slowGrowth(self):
            if level >= 100:
                level = 100
            else:
                requiredXP = ((5 * (n + 1) ** 3) / 4) - ((5 * (n) ** 3) / 4) 
                levelSetter(requiredXP)
        
            
 
class Move: 
    def __init__(self, power, damageType, type):
        self.power = power
        self.damageType = damageType
        self.type = type

    

class MoveSet:
    def __init__(self, move1, move2, move3, move4):
        self.move1 = move1
        self.move2 = move2
        self.move3 = move3
        self.move4 = move4

    def useMove1():
        return move1
    def useMove2():
        return move2
    def useMove3():
        return move3
    def useMove4():
        return move4
    

 
 
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
