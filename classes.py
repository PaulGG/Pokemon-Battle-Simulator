import random
import abc
import math
import time
import os

clear = lambda: os.system('cls')

class Player: 
    def __init__(self, pokemon, backpack): 
        self.pokemon = pokemon 
        self.backpack = backpack 
        for p in pokemon:
            if p.fainted is False:
                self.activePokemon = p
                break
 
class Backpack:
    def __init__(self, items):
        self.items = items

    def getAllItems(self):
        return self.items

    def useItem(self, index, user):
        self.items[index].use(user)
        del self.items[index]

class Item:
    def __init__(self, name):
        self.name = name

    @abc.abstractmethod
    def use(self, user):
        """Please define what the item will do in this function."""
        return

class HealingItem(Item):
    # Max is a boolean that determines if the item is supposed to fully restore the user's HP or not.
    def __init__(self, name, healthValue, max):
        Item.__init__(self, name)
        self.healthValue = healthValue
        self.max = max
    
    def use(self, user):
        if max:
            user.hp = user.maxHp
        else:
            user.hp += self.healthValue
        print("You used the " + self.name + ".")
        time.sleep(2)
        print("Restored " + user.name + "'s HP to " + str(user.hp) + ".")
        time.sleep(2)
        clear()
    
class FullRestore(HealingItem):
    def __init__(self):
        HealingItem.__init__(self, "Full Restore", 9999, True)

class Potion(HealingItem):
    def __init__(self, name):
        HealingItem.__init__(self, "Potion", 20, False)

class SuperPotion(HealingItem):
    def __init__(self):
        HealingItem.__init__(self, "Super Potion", 60, False)

class HyperPotion(HealingItem):
    def __init__(self):
        HealingItem.__init__(self, "Hyper Potion", 200, False)

class MaxPotion(HealingItem):
    def __init__(self):
        HealingItem.__init__(self, "Max Potion", 9999, True)

    def use(self, user):
        user.hp += 60
        print("You used the super potion.")
        time.sleep(2)
        print("Restored " + user.name + "'s HP to " + str(user.hp) + ".")
        time.sleep(2)
        clear()



class Pokemon:
    def __init__(self, name, hpStat, attackStat, defenseStat, spAttackStat, spDefenseStat, speedStat, level, moves, type1, type2, hpIV, 
        attackIV, defenseIV, spAttackIV, spDefenseIV, speedIV, hpEV, attackEV, defenseEV, spAttackEV, spDefenseEV, speedEV, nature, 
        growthRate, passive, healthStatus, itemHeld, wild): 
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
        self.healthStatus = "healthStatus"

        # item held....has effects
        self.itemHeld = itemHeld

        # All of these are calculated with mathematical equations
        self.hp = ((2 * hpStat + hpIV + hpEV / 4 + 100) * level) / 100 + 10
        self.maxHp = self.hp
        self.moves = moves
        self.attack = (((2 * attackStat + attackIV + attackEV / 4) * level) / 100 + 5) * nature
        self.defaultAttack = self.attack
        self.spAttack = (((2 * spAttackStat + spAttackIV + spAttackEV / 4) * level) / 100 + 5) * nature
        self.defaultSpAttack = self.spAttack
        self.defense = (((2 * defenseStat + defenseIV + defenseEV / 4) * level) / 100 + 5) * nature
        self.defaultDefense = self.defense
        self.spDefense = (((2 * spDefenseStat + spDefenseIV + spDefenseEV / 4) * level) / 100 + 5) * nature
        self.defaultSpDefense = self.spDefense
        self.speed = (((2 * speedStat + speedIV + speedEV / 4) * level) / 100 + 5) * nature
        self.defaultSpeed = self.speed

        self.fainted = True if self.hp <= 0 else False
        self.wild = wild

    def levelSetter(self, requiredXP):
        if self.xp >= requiredXP:
            leftoverXP = self.xp - requiredXP
            self.level += 1
            self.xp = 0 + leftoverXP

    def erraticGrowth(self):
        if self.level >= 100:
            self.level = 100
            return
        if self.level < 50:
            requiredXP = (((self.level + 1) ** 3 * (100 - self.level + 1)) / 50) - (((self.level) ** 3 * (100 - self.level)) / 50)
            self.levelSetter(requiredXP)
        elif self.level >= 50 and self.level < 68:
            requiredXP = (((self.level + 1) ** 3 * (150 - self.level + 1)) / 100) - (((self.level) ** 3 * (150 - self.level)) / 100)
            self.levelSetter(requiredXP)
        elif self.level >= 68 and self.level < 98:
            requiredXP = (((self.level + 1) ** 3 * math.floor((1911 - (10 * self.level + 1)) / 3)) / 500) - (((self.level) ** 3 
            * math.floor((1911 - (10 * self.level)) / 3)) / 500)
            self.levelSetter(requiredXP)
        elif self.level >= 98 and self.level > 100:
            requiredXP = (((self.level + 1) ** 3 * (160 - self.level + 1)) / 100) - (((self.level) ** 3 * (160 - self.level)) / 100)
            self.levelSetter(requiredXP)
    
    def fastGrowth(self):
        if self.level >= 100:
            self.level = 100
        else:
            requiredXP = ((4 * (self.level + 1) ** 3) / 5) - ((4 * (self.level) ** 3) / 5)
            self.levelSetter(requiredXP)

    def mediumFastGrowth(self):
        if self.level >= 100:
            self.level = 100
        else:
            requiredXP = (self.level + 1) ** 3 - self.level ** 3
            self.levelSetter(requiredXP)
    
    def mediumSlowGrowth(self):
        if self.level >= 100:
            self.level = 100
        else:
            requiredXP = (((6 / 5) * (self.level + 1) ** 3) - (15 * (self.level + 1) ** 2) + 100 * (self.level + 1) - 140) -\
            (((6 / 5) * (self.level) ** 3) - (15 * (self.level) ** 2) + 100 * (self.level) - 140)
            self.levelSetter(requiredXP)
    
    def slowGrowth(self):
        if self.level >= 100:
            self.level = 100
        else:
            requiredXP = ((5 * (self.level + 1) ** 3) / 4) - ((5 * (self.level) ** 3) / 4) 
            self.levelSetter(requiredXP)
    
class Move: 
    def __init__(self, name, power, accuracy, damageType, type, pp):
        self.name = name
        self.power = power
        self.accuracy = accuracy
        self.damageType = damageType
        self.type = type
        self.maxPP = pp
        self.pp = self.maxPP

    # TODO: fix
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
    
    #TODO: fix
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
    
    # TODO: FIX
    def determineSTAB(self, attacker, defender):
        #TODO: possibly make passive into an objet
        if attacker.passive is "adaptability":
            return 2
        elif self.type is attacker.type1 or type is attacker.type2:
            return 1.5
        else:
            return 1

    def determineEffectiveness(self, attacker, defender):
        if defender.type1 in self.type.typeImmunities or defender.type2 in self.type.typeImmunities:
            return 0
        elif defender.type1 in self.type.typeEffective or defender.type2 in self.type.typeEffective:
            if defender.type1 in self.type.typeEffective and defender.type2 in self.type.typeEffective:
                return 4
            elif defender.type1 in self.type.typeEffective and defender.type2 in self.type.typeNotEffective:
                return 1
            elif defender.type2 in self.type.typeEffective and defender.type1 in self.type.typeNotEffective:
                return 1
            else:
                return 2
        elif defender.type1 in self.type.typeNotEffective or defender.type2 in self.type.typeNotEffective:
            if defender.type1 in self.type.typeNotEffective and defender.type2 in self.type.typeNotEffective:
                return 0.25
            elif defender.type1 in self.type.typeEffective and defender.type2 in self.type.typeNotEffective:
                return 1
            elif defender.type2 in self.type.typeEffective and defender.type1 in self.type.typeNotEffective:
                return 1 
            else:
                return 0.5
       
        else: return 1

    #TODO: fix
    def determineBurn(self, attacker, defender):
        # TODO: healthStatus as object
        if attacker.healthStatus is "burned" and attacker.passive is not "guts" and self.damageType is "physical":
            return 0.5
        else: 
            return 1
    
    def damageFunc(self, attacker, defender, player, wild):
        delay = 2
        det = self.accuracy / 100
        det2 = random.random()
        if det2 > det:
            if player:
                print(attacker.name + " used " + self.name + "!")
                time.sleep(delay)
                print(attacker.name + " missed!")
                time.sleep(delay)
                clear()
            elif not wild:
                print("The enemy " + attacker.name + " used " + self.name + "!")
                time.sleep(delay)
                print("The enemy " + attacker.name + " missed!")
                time.sleep(delay)
                clear()
            else:
                print("The wild " + attacker.name + "used " + self.name + "!")
                time.sleep(delay)
                print("The wild " + attacker.name + " missed!")
            return
        targets = 1
        weather = self.determineWeatherMoveDamage()
        critical = self.determineCrit(attacker, defender)
        rando = self.determineRandom(attacker, defender)
        STAB = self.determineSTAB(attacker, defender)
        effectiveness = self.determineEffectiveness(attacker, defender)
        burn = self.determineBurn(attacker, defender)
        # TODO: other is an item effect
        other = 1

        if player:
            print(attacker.name + " used " + self.name + "!")
            time.sleep(delay)
        elif not wild:
            print("The enemy " + attacker.name + " used " + self.name + "!")
            time.sleep(delay)
        else:
            print("The wild " + attacker.name + " used " + self.name + "!")
            time.sleep(delay)
        if critical is not 1:
            print("A critical hit!")
            time.sleep(delay)
        if effectiveness is 0:
            print("It does not affect " + defender.name + "...")
            time.sleep(delay)
        elif effectiveness is 1:
            print("It had normal effectiveness.")
            time.sleep(delay)
        elif effectiveness > 1:
            print("It's super effective!")
            time.sleep(delay)
        elif effectiveness < 1:
            print("It's not very effective...")
            time.sleep(delay)

        clear()

        modifier = targets * weather * critical * rando * STAB * effectiveness * burn * other
        if self.damageType == "physical":
            defender.hp -= round(((((2 * attacker.level) / 5 + 2) * self.power * (attacker.attack / defender.defense)) / 50 + 2) * modifier)
            # Makes sure HP can never go below 0.
            if defender.hp <= 0:
                defender.hp = 0
                defender.fainted = True
        else: 
            defender.hp -= round(((((2 * attacker.level) / 5 + 2) * self.power * (attacker.spAttack / defender.spDefense)) / 50 + 2) * modifier)
            if defender.hp <= 0:
                defender.hp = 0
                defender.fainted = True
        
    def use(self, attacker, defender, player, wild):
            if self.pp <= 0:
                print("You don't have enough PP to use that move!")
                time.sleep(2)
                clear()
            else:
                self.pp -= 1
                return self.damageFunc(attacker, defender, player, wild)


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

    def reset(self):
        self.move1.pp = self.move1.maxPP
        self.move2.pp = self.move2.maxPP
        self.move3.pp = self.move3.maxPP
        self.move4.pp = self.move4.maxPP
class Type: 
    def __init__(self, typeName): 
        self.typeName = typeName 
    
    def __eq__(self, other):
        if other and self:
            return self.typeName is other.typeName
        else:
            return False
    
    def setEffectiveTypes(self, typeEffective):
        self.typeEffective = typeEffective
    
    def setNotEffectiveTypes(self, typeNotEffective):
        self.typeNotEffective = typeNotEffective
    
    def setImmuneTypes(self, typeImmunities):
        self.typeImmunities = typeImmunities
 
environment = Environment()