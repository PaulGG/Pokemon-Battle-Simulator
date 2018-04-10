class Human: 
    def __init__(self, pokemon, backpack): 
        self.pokemon = pokemon 
        self.backpack = backpack 
 
    def addItem(self): 
 
class Pokemon: 
    def __init__(self): 
 
class Move: 
 
 
class Type: 
    def __init__(self, typeName, typeEffective, typeNotEffective, typeImmunities): 
        self.typeName = typeName 
        self.typeEffective = typeEffective 
        self.typeNotEffective = typeNotEffective 
        self.typeImmunities = typeImmunities 
 
# Declaration of all pokemon types 
normal = Type(None, [rock, steel], [ghost]) 
fighting = Type([normal, rock, steel, ice, dark], [flying, poison, bug, psychic, fairy], ghost) 
flying = Type([fighting, bug, grass], [rock, steel, electric], None) 
poison = Type([grass, fairy], [poison, ground, rock, ghost], steel) 
ground = Type([poison, rock, steel, fire, electric], [bug, grass], flying) 
rock = Type([flying, bug, fire, ice], [fighting, ground, steel], None) 
bug = Type([grass, psychic, dark], [fighting, flying, poison, ghost, steel, fire, fairy], None) 
ghost = Type([ghost, psychic], [dark], normal) 
steel = Type([rock, ice, fairy], [steel, fire, water, electric], None) 
fire = Type([bug, steel, grass, ice], [rock, fire, water, dragon], None) 
water = Type([ground, rock, fire], [water, grass, dragon], None) 
grass = Type([ground, rock, water], [flying, poison, bug, steel, fire, grass, dragon], None) 
electric = Type([flying, water], [grass, electric, dragon], ground) 
psychic = Type([fighting, poison], [steel, psychic], dark) 
dragon = Type([dragon], [steel], fairy) 
dark = Type([ghost, psychic], [fighting, dark, fairy], None) 
fairy = Type([fighting, dragon, dark], [poison, steel, fire], None) 
 
# list of all types 
types = [normal, fighting, flying, poison, ground, rock, bug, ghost, steel, fire, water, grass, electric, psychic, dragon, dark, fairy]