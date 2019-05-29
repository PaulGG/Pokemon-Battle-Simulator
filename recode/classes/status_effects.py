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