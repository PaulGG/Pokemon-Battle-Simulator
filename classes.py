#pylint: disable=E1101

import random
import abc
import math
import time
import os
import copy
import pygame

pygame.mixer.init(48000, -16, 1, 1024)
def clear():
    if os.name == "nt":
        os.system('cls')
    elif os.name == "posix" or os.name == "mac":
        os.system("clear")
try:
    notEffective = pygame.mixer.Sound("sounds/not_effective.wav")
except pygame.error:
    notEffective = None
try:
    normalEffective = pygame.mixer.Sound("sounds/normal_effective.wav")
except pygame.error:
    normalEffective = None
try:
    superEffective = pygame.mixer.Sound("sounds/super_effective.wav")
except pygame.error:
    superEffective = None
try:
    useItemSound = pygame.mixer.Sound("sounds/use_item.wav")
except pygame.error:
    useItemSound = None
try:
    buyItem = pygame.mixer.Sound("sounds/bought_item.wav")
except pygame.error:
    buyItem = None

def sleep():
    time.sleep(2)

def playSound(sound):
    try:
        pygame.mixer.Sound.play(sound)
    except:
        None

class Player: 
    def __init__(self, pokemon, backpack, pc): 
        self.pokemon = pokemon 
        self.backpack = backpack 
        self.pc = pc
        self.money = 0
        if self.pokemon[0]:
            for p in pokemon:
                if p.fainted is False:
                    self.activePokemon = p
                    break
        else:
            self.activePokemon = None
    

    def setActivePokemon(self):
        if self.pokemon[0]:
            for p in self.pokemon:
                if p.fainted is False:
                    self.activePokemon = p
                    break
        else:
            self.activePokemon = None

    def takeMoney(self, amount):
        self.money -= amount
        if self.money < 0:
            self.money = 0
            print("You paid all your money to the winner...")
        print("You paid $" + str(amount) + " to the winner...")
    
    def giveMoney(self, amount):
        self.money += amount
        print("You were given $" + str(amount) + ".")
        sleep()
        clear()

    def getMoney(self):
        return self.money
 
class Backpack:
    def __init__(self, stacks):
        self.stacks = stacks

    def getItemStacks(self):
        return self.stacks

    def useItem(self, index, user):
        stack = list(self.stacks.values())[index]
        stack.item.use(user)
        stack.removeItem()
        if stack.amount <= 0:
            self.stacks.pop(stack.item.name, None)

    def addItem(self, item):
        stack = self.stacks.get(item.name)
        if not stack:
            self.stacks.update({item.name: Stack(item)})
        else:
            stack.addItem()

class Stack:
    def __init__(self, item):
        self.item = item
        self.amount = 1
    
    def addItem(self, amount=None):
        self.amount = self.amount + amount if amount else self.amount + 1
    
    def removeItem(self, amount=None):
        self.amount = self.amount - amount if amount else self.amount - 1

    def __str__(self):
        return self.item.name + " x " + str(self.amount)           

class Item:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    @abc.abstractmethod
    def use(self, user):
        """Please define what the item will do in this function."""
        return

    def buyItem(self, player):
        if(player.money - self.price >= 0):
            player.money -= self.price
            player.backpack.addItem(copy.deepcopy(self))
            playSound(buyItem)
            print("You purchased the " + self.name + ".")
            time.sleep(1)
            clear()
        else:
            print("You do not have enough money to afford the " + self.name + "!")
            sleep()
            clear()

class GenericPokeBall(Item):
    def __init__(self, name, catchRate, price):
        Item.__init__(self, name, price)
        self.catchRate = catchRate

class PokeBall(GenericPokeBall):
    def __init__(self):
        # TODO: fix prices for all poke ball variants
        GenericPokeBall.__init__(self, "Poke Ball", 1, 100)
    
    def use(self, user=None):
        return

class GreatBall(GenericPokeBall):
    def __init__(self):
        GenericPokeBall.__init__(self, "Great Ball", 1.5, 200)

    def use(self, user=None):
        return

class UltraBall(GenericPokeBall):
    def __init__(self):
        GenericPokeBall.__init__(self, "Ultra Ball", 2, 500)
    
    def use(self, user=None):
        return

class MasterBall(GenericPokeBall):
    def __init__(self):
        GenericPokeBall.__init__(self, "Master Ball", 255, 10000)

    def use(self, user=None):
        return

class RevivalItem(Item):
    def __init__(self, name, reviveLevel, price):
        Item.__init__(self, name, price)
        self.reviveLevel = reviveLevel
    
    def use(self, user):
        hpToRestore = user.maxHp * self.reviveLevel
        user.hp += hpToRestore
        user.fainted = False
        playSound(useItemSound)
        print("You used the " + self.name + ".")
        print("Revived " + user.name + ".")

class Revive(RevivalItem):
    def __init__(self):
        RevivalItem.__init__(self, "Revive", 0.5, 1500)
        
class MaxRevive(RevivalItem):
    def __init__(self):
        RevivalItem.__init__(self, "Revive", 1, 2000)

class HealingItem(Item):
    # Max is a boolean that determines if the item is supposed to fully restore the user's HP or not.
    def __init__(self, name, max, price, healthValue=None):
        Item.__init__(self, name, price)
        self.healthValue = healthValue
        self.max = max
    
    def use(self, user):
        if max:
            user.hp = user.maxHp
        else:
            user.hp += self.healthValue
        print("You used the " + self.name + ".")
        sleep()
        print("Restored " + user.name + "'s HP to " + str(user.hp) + ".")
        sleep()
        clear()
    
class FullRestore(HealingItem):
    def __init__(self):
        HealingItem.__init__(self, "Full Restore", True, 3000)

class Potion(HealingItem):
    def __init__(self):
        HealingItem.__init__(self, "Potion", False, 300, 20)

class SuperPotion(HealingItem):
    def __init__(self):
        HealingItem.__init__(self, "Super Potion", False, 700, 60)

class HyperPotion(HealingItem):
    def __init__(self):
        HealingItem.__init__(self, "Hyper Potion", False, 1200, 200)

class MaxPotion(HealingItem):
    def __init__(self):
        HealingItem.__init__(self, "Max Potion", True, 2500)

    def use(self, user):
        HealingItem.use(self, user)
        user.healthStatus = "normal"

class Pokemon:
    def __init__(self, name, hpStat, attackStat, defenseStat, spAttackStat, spDefenseStat, speedStat, level, moves, type1, type2, hpIV, 
        attackIV, defenseIV, spAttackIV, spDefenseIV, speedIV, hpEV, attackEV, defenseEV, spAttackEV, spDefenseEV, speedEV, nature, 
        growthRate, passive, itemHeld, wild): 
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
        self.healthStatus = Normal(self)

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
        self.cannotAttack = False

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

# How will these work in battle?
# At the end of the player's turn, or right before the player's turn, the game will check to see if 
# any status effects are present. If there is one, then we will need to see what specifically it is.
# We will make a function in the main game file that will handle what occurrs when we need to parse 
# what a status effect does. For example, Paralysis would make it so the user might not be able to attack.
# It would also make the user's speed terrible. 

# the game loop needs to get refactored in the way things are done before I can continue with status effects.
class StatusEffect:
    def __init__(self, name, victim):
        self.name = name
        self.victim = victim
    
    @abc.abstractclassmethod
    def effects(self, victim):
        print("Please implement this!")

class Normal(StatusEffect):
    def __init__(self, victim):
        StatusEffect.__init__(self, "normal", victim)

    def effects(self, victim):
        return True

class Paralysis(StatusEffect):
    def __init__(self, victim):
        StatusEffect.__init__(self, "paralysis", victim)
        self.victim.speed /= 2.0

    def effects(self, victim):
        rando = random.random()
        if rando >= 0 and rando <= 0.25:
            print(victim.name + " is paralyzed! It can't move!")
            sleep()
            clear()
            return False
        return True

    def __del__(self):
        self.victim.speed *= 2
        self.victim.healthStatus = Normal(self.victim)

class Frozen(StatusEffect):
    def __init__(self, victim):
        StatusEffect.__init__(self, "frozen", victim)

    def effects(self, victim):
        rando = random.random()
        if rando >= 0 and rando <= .2:
            print(victim.name + " thawed out!")
            sleep()
            clear()
            return True
        else:
            print(victim.name + " is frozen!")
            sleep()
            clear()
            return False

class Confusion(StatusEffect):
    def __init__(self, victim):
        StatusEffect.__init__(self, "confusion", victim)
        self.turns = round(5.0 * random.random())

    def effects(self, victim):
        rando = random.random()
        print(victim.name + " is confused!")
        sleep()
        clear()
        if self.turns <= 0:
            print(victim.name + " snapped out of confusion!")
            sleep()
            clear()
            victim.healthStatus = Normal(victim)
            return True
        if rando >= 0 and rando <= .5:
            # ((((2A/5 + 2)*B*40)/C)/50) + 2
            victim.hp -= round(((((2*victim.level/5 + 2)*victim.attackStat*40)/victim.defenseStat)/50) + 2)
            if victim.hp <= 0:
                victim.hp = 0
                victim.fainted = True
            print(victim.name + " hurt itself in its confusion!")
            sleep()
            clear()
            self.turns -= 1
            return False
        self.turns -= 1
        return True

class Flinch(StatusEffect):
    def __init__(self, victim):
        StatusEffect.__init__(self, "flinch", victim)

    def effects(self, victim):
        print(victim.name + " flinched!")
        sleep()
        clear()
        victim.healthStatus = Normal(victim)
        return False


class Infatuation(StatusEffect):
    def __init__(self, victim):
        StatusEffect.__init__(self, "infatuation", victim)

    def effects(self):
        print("TODO")

class Poisoned(StatusEffect):
    def __init__(self, victim):
        StatusEffect.__init__(self, "poisoned", victim)

    def effects(self):
        print("TODO")

class BadlyPoisoned(StatusEffect):
    def __init__(self, victim):
        StatusEffect.__init__(self, "badlypoisoned", victim)

    def effects(self):
        print("TODO")
        
class Burned(StatusEffect):
    def __init__(self, victim):
        StatusEffect.__init__(self, "burned", victim)

    def effects(self):
        print("TODO")



class LeechSeed(StatusEffect):
    def __init__(self, victim):
        StatusEffect.__init__(self, "leechseed", victim)

    def effects(self):
        print("TODO")

class Move: 
    def __init__(self, name, power, accuracy, damageType, type, pp):
        self.name = name
        self.power = power
        self.accuracy = accuracy
        # What are the different properties of moves?
        # 1. Physical
        # 2. Special
        # 3. Status Effects (burn, paralysis, sleep)
        # 4. 1 Hit KO
        # 5. Healing moves
        # 6. Stat effect moves (temporarily boost speed, attack, defense, or lower)
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
        det = float(self.accuracy / 100.0)
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

        def checkCritical(critical, effectiveness):
            if critical is not 1 and effectiveness is not 0:
                print("A critical hit!")
                time.sleep(delay)

        if player:
            print(attacker.name + " used " + self.name + "!")
            time.sleep(delay / 2)
        elif not wild:
            print("The enemy " + attacker.name + " used " + self.name + "!")
            time.sleep(delay)
        else:
            print("The wild " + attacker.name + " used " + self.name + "!")
            time.sleep(delay)
        if self.damageType == "special" or self.damageType == "physical":
            if effectiveness is 0:
                print("It does not affect " + defender.name + "...")
                time.sleep(delay)
            elif effectiveness is 1:
                playSound(normalEffective)
                time.sleep(delay)
                checkCritical(critical, effectiveness)
                print("It had normal effectiveness.")
                time.sleep(delay)
            elif effectiveness > 1:
                playSound(superEffective)
                time.sleep(delay)
                checkCritical(critical, effectiveness)
                print("It's super effective!")
                time.sleep(delay)
            elif effectiveness < 1:
                playSound(notEffective)
                time.sleep(delay)
                checkCritical(critical, effectiveness)
                print("It's not very effective...")
                time.sleep(delay)
        elif self.damageType == "onehitko":
            print("Oof! It's a one-hit KO!")
            time.sleep(delay)
        elif self.damageType == "statchange":
            print("TODO")
        elif self.damageType == "statuseffect":
            print("TODO")
        else:
            print("TODO")

        clear()

        modifier = targets * weather * critical * rando * STAB * effectiveness * burn * other
        if self.damageType == "physical":
            defender.hp -= round(((((2 * attacker.level) / 5 + 2) * self.power * (attacker.attack / defender.defense)) / 50 + 2) * modifier)
            # Makes sure HP can never go below 0.
            if defender.hp <= 0:
                defender.hp = 0
                defender.fainted = True
        elif self.damageType == "special": 
            defender.hp -= round(((((2 * attacker.level) / 5 + 2) * self.power * (attacker.spAttack / defender.spDefense)) / 50 + 2) * modifier)
            if defender.hp <= 0:
                defender.hp = 0
                defender.fainted = True
        elif self.damageType == "onehitko":
            defender.hp = 0
            defender.fainted = True
        
    def use(self, attacker, defender, player, wild):
            if self.pp <= 0:
                print("You don't have enough PP to use that move!")
                sleep()
                clear()
                return
            # This function returns true if the attacker is able to attack. False if some status effect prohibits it.
            if attacker.healthStatus.effects(attacker):
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

    def getMove1(self):
        return self.move1
    def getMove2(self):
        return self.move2
    def getMove3(self):
        return self.move3
    def getMove4(self):
        return self.move4

    def getMovesInArray(self):
        return [self.move1, self.move2, self.move3, self.move4]

    def size(self):
        size = 0
        for m in self.getMovesInArray():
            if m is not None:
                size += 1
        return size

    def reset(self):
        self.move1.pp = self.move1.maxPP
        self.move2.pp = self.move2.maxPP
        if self.move3:
            self.move3.pp = self.move3.maxPP
            if self.move4:
                self.move4.pp = self.move4.maxPP
class Type: 
    def __init__(self, typeName): 
        self.typeName = typeName 
    
    def __eq__(self, other):
        if other and self:
            if isinstance(other, Type):
                return self.typeName == other.typeName
            else:
                return False
        else:
            return False
    
    def setEffectiveTypes(self, typeEffective):
        self.typeEffective = typeEffective
    
    def setNotEffectiveTypes(self, typeNotEffective):
        self.typeNotEffective = typeNotEffective
    
    def setImmuneTypes(self, typeImmunities):
        self.typeImmunities = typeImmunities
 
environment = Environment()