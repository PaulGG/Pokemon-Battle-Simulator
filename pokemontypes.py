from classes import Type

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
types = [normal, fighting, flying, poison, ground, rock, bug, ghost, steel, fire, water, grass, electric, psychic, dragon, dark, fairy]
setTypes(fighting, [normal, rock, steel, ice, dark], [flying, poison, bug, psychic, fairy], [ghost])
setTypes(flying, [fighting, bug, grass], [rock, steel, electric], [None])
setTypes(poison, [grass, fairy], [poison, ground, rock, ghost], [steel])
setTypes(ground, [poison, rock, steel, fire, electric], [bug, grass], [flying])
setTypes(rock, [flying, bug, fire, ice], [fighting, ground, steel], [None])
setTypes(bug, [grass, psychic, dark], [fighting, flying, poison, ghost, steel, fire, fairy], [None])
setTypes(ghost, [ghost, psychic], [dark], [normal])
setTypes(steel, [rock, ice, fairy], [steel, fire, water, electric], [None])
setTypes(fire, [bug, steel, grass, ice], [rock, fire, water, dragon], [None])
setTypes(water, [ground, rock, fire], [water, grass, dragon], [None])
setTypes(grass, [ground, rock, water], [flying, poison, bug, steel, fire, grass, dragon], [None])
setTypes(electric, [flying, water], [grass, electric, dragon], [ground])
setTypes(psychic, [fighting, poison], [steel, psychic], [dark])
setTypes(ice, [flying, ground, grass, dragon], [steel, fire, water, ice], [dark])
setTypes(dragon, [dragon], [steel], [fairy])
setTypes(dark, [ghost, psychic], [fighting, dark, fairy], [None])
setTypes(fairy, [fighting, dragon, dark], [poison, steel, fire], [None])

# list of all types 
