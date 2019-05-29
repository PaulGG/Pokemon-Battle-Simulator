from pokepy import V2Client
from functions import io
from classes.pokemon import Pokemon

def choose_starter():
    starter_gen = io.r_int(
        "Please select one of these generations", strarray=[
        "There are several starter generations to choose from.",
        "1: Kanto, Generation 1 (Bulbasaur, Charmander, Squirtle, Pikachu)",
        "2: Johto, Generation 2 (Chikorita, Cyndaquil, Totodile)",
        "3: Hoenn, Generation 3 (Treecko, Torchic, Mudkip)",
        "4: Sinnoh, Generation 4 (Turtwig, Chimchar, Piplup",
        "5: Unova, Generation 5 (Snivy, Tepig, Oshawott",
        "6: Kalos, Generation 6 (Chespin, Fennekin, Froakie)",
        "7: Alola, Generation 7 (Rowlet, Litten, Popplio)"
        ], min=1, max=7
    )
    if starter_gen is 1:
        options = {
            1: "Bulbasaur",
            2: "Charmander",
            3: "Squirtle",
            4: "Pikachu"
        }

        starter_num = io.r_int(
            "Choose your starter",
            strarray=generate_starter_selection(options, 4), 
            min=1, max=4
        )
        starter_choice = options[starter_num]
    elif starter_gen is 2:
        options = {
            1: "Chikorita",
            2: "Cyndaquil",
            3: "Totodile"
        }
        
        starter_num = io.r_int(
            "Choose your starter",
            strarray=generate_starter_selection(options, 3), 
            min=1, max=3
        )
        starter_choice = options[starter_num]
    elif starter_gen is 3:
        options = {
            1: "Treecko",
            2: "Torchic",
            3: "Mudkip"
        }
        
        starter_num = io.r_int(
            "Choose your starter",
            strarray=generate_starter_selection(options, 3), 
            min=1, max=3
        )
        starter_choice = options[starter_num]
    elif starter_gen is 4:
        options = {
            1: "Turtwig",
            2: "Chimchar",
            3: "Piplup"
        }
        
        starter_num = io.r_int(
            "Choose your starter",
            strarray=generate_starter_selection(options, 3), 
            min=1, max=3
        )
        starter_choice = options[starter_num]
    elif starter_gen is 5:
        options = {
            1: "Snivy",
            2: "Tepig",
            3: "Oshawott"
        }
        
        starter_num = io.r_int(
            "Choose your starter",
            strarray=generate_starter_selection(options, 3), 
            min=1, max=3
        ) 
        starter_choice = options[starter_num]
    elif starter_gen is 6:
        options = {
            1: "Chespin",
            2: "Fennekin",
            3: "Froakie"
        }
        
        starter_num = io.r_int(
            "Choose your starter",
            strarray=generate_starter_selection(options, 3), 
            min=1, max=3
        )
        starter_choice = options[starter_num]
    elif starter_gen is 7:
        options = {
            1: "Rowlet",
            2: "Litten",
            3: "Popplio"
        }
        
        starter_num = io.r_int(
            "Choose your starter",
            strarray=generate_starter_selection(options, 3), 
            min=1, max=3
        )
        starter_choice = options[starter_num]
    io.w("You choose {}!".format(starter_choice))

    pokeapi = V2Client()

    s = pokeapi.get_pokemon(starter_choice)
    species = pokeapi.get_pokemon_species(starter_choice)

    isSecondary = len(s.types) > 1 
    if len(s.types) > 1:
        if types[0].slot is 2:
            secondary_type = types[0].type.name
            primary_type = types[1].type.name
        else:
            primary_type = types[0].type.name
            secondary_type = types[1].type.name
    else:
        primary_type = types[0].type.name
        secondary_type = None


    starter = Pokemon(s.name, s.stats[5].base_stat, s.stats[4].base_stat, 
                s.stats[3].base_stat, s.stats[2].base_stat, s.stats[1].base_stat, 
                s.stats[0].base_stat, s.moves, primary_type, secondary_type, species.growth_rate, wild=False
                )
    
def generate_starter_selection(options, number):
    return [
        "{}: {}".format(i, options[i])
    for i in range(1, number + 1)]