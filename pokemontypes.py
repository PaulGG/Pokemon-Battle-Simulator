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
types = {normal.typeName.lower(): normal, fighting.typeName.lower(): fighting, flying.typeName.lower(): flying, poison.typeName.lower(): poison, 
    ground.typeName.lower(): ground, rock.typeName.lower(): rock, bug.typeName.lower(): bug, ghost.typeName.lower(): ghost, 
    steel.typeName.lower(): steel, fire.typeName.lower(): fire, water.typeName.lower(): water, grass.typeName.lower(): grass,
    electric.typeName.lower(): electric, psychic.typeName.lower(): psychic, dragon.typeName.lower(): dragon, dark.typeName.lower(): dark, fairy.typeName.lower(): fairy, ice.typeName.lower(): ice}
setTypes(normal, [None], [rock, steel], [ghost])
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
