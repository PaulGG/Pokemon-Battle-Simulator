from classes.status_effects import Normal

class Pokemon:
    def __init__(self, name, hpStat, attackStat, defenseStat, spAttackStat, spDefenseStat, speedStat, level, moves_list, type1, type2,  
        growthRate, passive, itemHeld, wild): 
        self.name = name
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

        # A pokemon's nature must be https://pokemondb.net/mechanics/natures
        self.nature = nature

        # A pokemon's growth rate (Level) is determined if it is Erratic, Fast, Medium Fast, Medium Slow, or Slow
        self.growthRate = growthRate
        self.xp = 0

        # Initial level for a pokemon
        self.level = level

        # health status is like burn, paralyzed, etc.
        self.healthStatus = Normal(self)

        # item held....has effects
        self.itemHeld = itemHeld

        # All of these are calculated with mathematical equations
        self.hp = ((2 * hpStat + hpIV + hpEV / 4 + 100) * level) / 100 + 10
        self.maxHp = self.hp

        self.moves_list = moves_list

        # TODO self.moves = make_moveset(self.moves_list)
        
        
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