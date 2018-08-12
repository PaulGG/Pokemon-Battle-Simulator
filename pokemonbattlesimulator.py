#pylint: disable=E1101

import random
import copy
from classes import *
from pokemontypes import flying, poison, ground, rock, fire, grass, dragon, types, water, ice
import os
import time
import pickle
import sys
import pygame
import sys

try:
    ss = pygame.mixer.Sound("sounds/select_sound.wav")
except pygame.error:
    print("Warning: Sound Files Missing")
    time.sleep(2)
    clear()
    ss = None

def selectSound():
    try:
        pygame.mixer.Sound.play(ss)
    except:
        None

def readData(filename, defaultData):
    if not os.path.exists(filename):
        open(filename, "w")
        with open(filename, "wb") as output:
            pickle.dump(defaultData, output, pickle.HIGHEST_PROTOCOL)
    try:
        with open(filename, "rb") as inpuut:
            return pickle.load(inpuut)
    except EOFError:
        open(filename, "w")
        with open(filename, "wb") as output:
            pickle.dump(defaultData, output, pickle.HIGHEST_PROTOCOL)

def writeData(filename, data):
    with open(filename, "wb") as output:
        pickle.dump(data, output, pickle.HIGHEST_PROTOCOL)

def selectBattle():
    options = [
        "1. Trainer Pokemon Battle", 
        "2. Wild Pokemon Battle", 
        "3. Go Back"
        ]
    wildOrNot = getInputWithConstraints("Please say if you would like to have a wild pokemon battle or a trainer battle. ", True, options, 1, 3)
    if wildOrNot is not 3:
        startBattle(wildOrNot - 1)
    else:
        return
    battleAgain(options)

def getTextInput(message):
    while True:
        try:
            usrInput = input(message)
            selectSound()
            confirm = input("Your input is " + usrInput + ". Are you sure? (type y to continue) ")
            selectSound()
            clear()
            if confirm == "y":
                return usrInput
        except ValueError:
            clear()
            print("Invalid input!")
            sleep()
            clear()

def getInputWithConstraints(message, exitable, options=None, min=None, max=None, double=None):
    while True:
        if options:
            for o in options:
                print(o)
        try:
            usrInput = input(message)
            if usrInput == "~" and exitable: 
                clear()
                selectSound()
                return usrInput
            if double:
                usrInput = float(usrInput)
            else:
                usrInput = int(usrInput)
            selectSound()
            if min and max: 
                if usrInput < min or usrInput > max:
                    raise ValueError
            clear()
            return usrInput
        except ValueError:
            clear()
            print("Invalid input!")
            sleep()
            clear()

def getMoveInput(num):
    if num is not 1 and num is not 2:
        if num is 3 or 4:
            while True:
                try:
                    usrInput = input("Do you want this Pokemon to have another move? (y/n) ")
                    selectSound()
                    if usrInput == "y":
                        break
                    elif usrInput == "n":
                        return
                    else: 
                        raise ValueError
                except ValueError:
                    clear()
                    print("Invalid input!")
                    sleep()
                    clear()
    name = getTextInput("Please enter the name of move " + str(num) + ". (~ to exit) ")
    if name == "~": 
        clear()
        return "~"
    move = movesDatabase.get(name.lower())
    if move:
        print("This move already exists in the database.")
        sleep()
        clear()
        return move
    while True:
        upType = getTextInput("Please enter the Pokemon type of this move. (~ to exit) ")
        if upType == "~": 
            clear()
            return "~"
        if types.get(upType.lower()):
            pType = types.get(upType.lower())
            break
        print("That isn't a valid type.")
        sleep()
        clear()
        # getInputWithConstraints(message, exitable, options=None, min=None, max=None, double=None)
    dmgType = getInputWithConstraints("Please enter damage type: physical, special, one hit KO, healing, stat change, health status effect (~ for exit) ", True, ["1. Special", "2. Physical", "3. One Hit KO", "4. Healing", "5. Stat Change", "6. Health Status Effect"], 1, 6)
    
    switcher = {
        1: "physical",
        2: "special", 
        3: "onehitko",
        4: "healing",
        5: "statchange",
        6: "statuseffect"
    }

    dmgType = switcher.get(dmgType)

    if dmgType == "~": 
        clear()
        return "~"
    accuracy = getInputWithConstraints("Please enter an accuracy value (10 to 100) (~ for exit) ", True, None, 10, 100)
    if accuracy == "~": 
        clear()
        return "~"
    damage = None
    if dmgType != "onehitko":
        damage = getInputWithConstraints("Please enter a damage value (50 to 150) (~ for exit) ", True, None, 50, 150)
        if damage == "~": 
            clear()
            return "~"
    else:
        damage = 150
    PP = getInputWithConstraints("Please enter the power point (PP) value (5 to 50) (~ for exit) ", True, None, 5, 50)
    if PP == "~": 
        clear()
        return "~"
    return Move(name, damage, accuracy, dmgType, pType, PP)

def getMovesInput():
    move1 = getMoveInput(1)
    if move1 == "~":
        return "~"
    movesDatabase.update({move1.name: move1})
    move2 = getMoveInput(2)
    if move2 == "~":
        return "~"
    movesDatabase.update({move2.name: move2})
    move3 = getMoveInput(3)
    if move3 == "~":
        return "~"
    if move3:
        movesDatabase.update({move3.name: move3})
        move4 = getMoveInput(4)
        if move4 == "~":
            return "~"
        if move4:
            movesDatabase.update({move4.name: move4})
        else:
            move4 = None
    else:
        move3 = None
        move4 = None
    writeData("moves_data.pkl", movesDatabase)
    return MoveSet(move1, move2, move3, move4)
    
def typeInput(msg, prim):
    while True:
        usrIn = getTextInput(msg)
        if usrIn.lower() == "none" and prim is not 1:
            return None
        elif usrIn.lower() == "none":
            print("You must have a primary type. ")
            sleep()
            clear()
            continue
        usrType = types.get(usrIn.lower())
        if usrType:
            return usrType
        print("Type not recognized.")
        sleep()
        clear()

def pokeShop():
    def itemChooser(args):
        switcher = {
            1: Potion,
            2: SuperPotion,
            3: HyperPotion,
            4: MaxPotion,
            5: FullRestore,
            6: Revive,
            7: MaxRevive,
            8: PokeBall,
            9: GreatBall,
            10: UltraBall,
            11: MasterBall
        }
        if args is 12:
            return False
        else:
            switcher.get(args, invalid)().buyItem(player)
            return True
    try:
        pygame.mixer.music.load("sounds/shop_theme.wav")
        pygame.mixer.music.play(loops=-1)
    except pygame.error:
        None
    print("Welcome to the Pokemart.")
    sleep()
    clear()
    myBool = True
    while myBool:
        options = ["Current Money Balance: $" + str(player.getMoney()), "-----------------------------", "1. Potion - restores 20 HP. $300", 
        "2. Super Potion - restores 60 HP. $700", 
        "3. Hyper Potion - restores 200 HP. $1200", 
        "4. Max Potion - restores max HP. $2500", 
        "5. Full Restore - restores max HP and clears status effects. $3000", 
        "6. Revive - heals a fainted Pokemon halfway. $1500", 
        "7. Max Revive - heals a fainted pokemon completely. $2000", 
        "8. Poke Ball - standard item for catching pokemon. $100",
        "9. Great Ball - slightly higher catch rate. $200",
        "10. Ultra Ball - double the catch rate of the normal Poke ball. $500",
        "11. Master Ball - Catches any pokemon without fail. $10000",
        "12. Go back"]
        usrIn = getInputWithConstraints("Please select an item you would like to purchase. ", False, options, 1, 12)
        myBool = itemChooser(usrIn)
        writeData("player_data.pkl", player)
    try:
        pygame.mixer.music.load("sounds/main_theme.wav")
        pygame.mixer.music.play(loops=-1)
    except pygame.error:
        None
    
def createPokemon():
    clear()
    print("Create your own Pokemon here!")
    print("Pokemon made here will be saved to the file.")
    print("It is advised that you take legitimate pokemon from the original game and put them in.")
    print("Don't make ridiculously overpowered/underpowred Pokemon! Normally pokemon have base stats between 50-120.")
    print("Enemies will be randomly assigned pokemon in the save game. If you make an overpowered pokemon, then the enemy might get it!")
    name = getTextInput("Please enter the name of the pokemon that you would like to create. (~ to exit) ")
    if name == "~": return
    newPokemon = pokemonDatabase.get(name.lower())
    if newPokemon:
        print("This pokemon is already in the database.")
        sleep()
        clear()
        return
    hpStat = getInputWithConstraints("Please enter the HP stat. (between 1-255) (~ to exit) ", True, None, 1, 255)
    if hpStat == "~": 
        clear()
        return
    attackStat = getInputWithConstraints("Please enter the attack stat. (between 1-255) (~ to exit) ", True, None, 1, 255)
    if attackStat == "~":
        clear()
        return
    defenseStat = getInputWithConstraints("Please enter the defense stat. (between 1-255) (~ to exit) ", True, None, 1, 255)
    if defenseStat == "~": 
        clear()
        return
    spAttackStat = getInputWithConstraints("Please enter the special attack stat. (between 1-255) (~ to exit) ", True, None, 1, 255)
    if spAttackStat == "~": 
        clear()
        return
    spDefenseStat = getInputWithConstraints("Please enter the special defense stat. (between 1-255) (~ to exit) ", True, None, 1, 255)
    if spDefenseStat == "~": 
        clear()
        return
    speedStat = getInputWithConstraints("Please enter the speed stat. (between 1-255) (~ to exit) ", True, None, 1, 255)
    if speedStat == "~": 
        clear()
        return
    moves = getMovesInput()
    if moves == "~": 
        clear()
        return
    type1 = typeInput("Please enter the pokemon's primary type. (~ to exit) ", 1)
    if type1 == "~": 
        clear()
        return
    type2 = typeInput("Please enter the pokemon's secondary type. If it does not have one, type 'none'. (~ to exit) ", 2)
    if type2 == "~": 
        clear()
        return
    hpIV = round(random.random() * 31)
    attackIV = round(random.random() * 31)
    defenseIV = round(random.random() * 31)
    spAttackIV = round(random.random() * 31)
    spDefenseIV = round(random.random() * 31)
    speedIV = round(random.random() * 31)
    hpEV = round(random.random() * 252)
    attackEV = round(random.random() * 252)
    defenseEV = round(random.random() * 252)
    spAttackEV = round(random.random() * 252)
    spDefenseEV = round(random.random() * 252)
    speedEV = round(random.random() * 252)
    # worry about nature later
    nature = 1.0
    # worry about this later
    growthRate = None#input("Please enter the pokemon's growth rate.")
    passive = None#input("Please enter your pokemon's passive.")
    itemHeld = None
    level = getInputWithConstraints("Please enter the level for the Pokemon. (1 to 100) (~ to exit) ", True, None, 1, 100)
    if level == "~": 
        clear()
        return
    newPokemon = Pokemon(name, hpStat, attackStat, defenseStat, spAttackStat, spDefenseStat, speedStat, level, moves, type1, type2, hpIV, 
        attackIV, defenseIV, spAttackIV, spDefenseIV, speedIV, hpEV, attackEV, defenseEV, spAttackEV, spDefenseEV, speedEV, nature, 
        growthRate, passive, itemHeld, False)
    pokemonDatabase.update({newPokemon.name.lower(): newPokemon})
    writeData("pokemon_data.pkl", pokemonDatabase)
    clear()

def printPokemonWithEmptySlots(pokemon, goBack):
    for i in range (1, len(pokemon) + 1):
        if pokemon[i - 1] is not None:
            print(str(i) + ". " + pokemon[i - 1].name)
        else:
            print(str(i) + ". Empty Slot")
    if goBack:
        i += 1
        print(str(i) + ". Go Back")


# this SHOULD be working.
def sort(pokemon):
    # need to get rid of all gaps in between list...how do we do this
    # for each item in the list, if it is none, swap with the next?
    for i in range(0, 4):
        if pokemon[i] is None:
            temp = pokemon[i + 1]
            pokemon[i + 1] = pokemon[i]
            pokemon[i] = temp
    # 0, 1, 2, 3, 4, 5. The 5th can be none, that is OK

def getPokemonAsOptions(pokemon):
    options = []
    for i in range(1, len(pokemon) + 1):
        if pokemon[i - 1] is not None:
            options.append(str(i) + ". " + pokemon[i - 1].name)
        else:
            options.append(str(i) + ". Empty")
    j = i + 1
    options.append(str(j) + ". Go Back")
    return options

def viewPokemonPC():
    clear()
    print("Welcome to the PC. Here, all your pokemon are stored.")
    sleep()
    clear()
    while True:
        options = [
            "1. Deposit Pokemon", 
            "2. Withdraw Pokemon", 
            "3. Move Pokemon",
            "4. Go Back"
            ]
        usrIn = getInputWithConstraints("Please select one of the above options. ", False, options, 1, 4)
        if usrIn is 1:
            sumOfPokemon = 0
            for p in player.pokemon:
                if p is not None:
                    sumOfPokemon += 1
            if sumOfPokemon <= 1:
                print("You must have at least one pokemon in your team at all times, and you only have one!")
                sleep()
                clear()
                continue
            while True:
                printPokemonWithEmptySlots(player.pokemon, False)
                pDeposit = getInputWithConstraints("Please select a pokemon to deposit (~ to exit). ", True, None, 1, 6)
                if pDeposit is "~":
                    return
                if player.pokemon[pDeposit - 1] is None:
                    print("You can't deposit an empty slot. ")
                    sleep()
                    clear()
                else:
                    player.pc.append(player.pokemon[pDeposit - 1])
                    player.pokemon[pDeposit - 1] = None
                    sort(player.pokemon)
                    break
        elif usrIn is 2:
            if len(player.pc) is 0:
                print("You don't have any pokemon in the PC to withdraw!")
                sleep()
                clear()
                continue
            check = True
            for p in player.pokemon:
                if p is None:
                    check = False
                    break
            if check:
                print("You cannot withdraw any pokemon because your team is full!")
            else:
                printPokemonWithEmptySlots(player.pc, False)
                pWithdraw = getInputWithConstraints("Please select a pokemon to withdraw. ", False, getPokemonAsOptions(player.pokemon), 1, len(player.pc) + 1)
                if pWithdraw is len(player.pc) + 1:
                    return
                # ask for input
                selectedPokemon = player.pc[pWithdraw - 1]
                pInsert = getInputWithConstraints("Please select a position on your team to insert this pokemon. ", False, getPokemonAsOptions(player.pokemon), 1, 7)
                if pInsert is 7:
                    return
                # if the user inputs a position where a pokemomn already is, say we can't do that.
                if player.pokemon[pInsert - 1] is not None:
                    print("You cannot withdraw a Pokemon into a slot that is occupied!")
                # if the user inputs an empty position, put the pokemon there.
                else:
                    player.pokemon[pInsert - 1] = selectedPokemon
                    sort(player.pokemon)
                # remove from PC.
                player.pc.remove(selectedPokemon)
        elif usrIn is 3:
            # User can do two things: Swap around pokemon in their own team, or they can swap pokemon from their team and box.
            while True:
                options = [
                    "1. Swap Pokemon around in team",
                    "2. Swap Pokemon around in box", 
                    "3. Swap pokemon around in team and box",
                    "4. Go Back"
                ]
                opt = getInputWithConstraints("Please select one of the options. " , False, options, 1, 4)
                if opt is 4:
                    break
                # 1. Swap pokemon around in team
                if opt is 1:
                    while True:
                        swap1 = getInputWithConstraints("Please select a Pokemon. " , False, getPokemonAsOptions(player.pokemon), 1, 7)
                        if swap1 is 7:
                            break
                        if player.pokemon[swap1 - 1] is None:
                            clear()
                            print("You cannot select an empty slot to swap.")
                            sleep()
                            clear()
                            break
                        swap2 = getInputWithConstraints("Please select a Pokemon to swap. ", False, getPokemonAsOptions(player.pokemon), 1, 7)
                        if swap1 is 7:
                            break
                        if player.pokemon[swap2 - 1] is None:
                            clear()
                            print("You cannot select an empty slot to swap.")
                            sleep()
                            clear()
                            break
                        if swap1 is swap2:
                            clear()
                            print("You can't swap a pokemon with itself.")
                            sleep()
                            clear()
                            break
                        else:
                            temp = player.pokemon[swap1 - 1]
                            player.pokemon[swap1 - 1] = player.pokemon[swap2 - 1]
                            player.pokemon[swap2 - 1] = temp
                            break
                # 2. Swap pokemon around in box
                elif opt is 2:
                    while True:
                        if len(player.pc) <= 0:
                            print("You do not have any Pokemon in your PC!")
                            sleep()
                            clear()
                            break 
                        swap1 = getInputWithConstraints("Please selet a Pokemon to swap. ", False, getPokemonAsOptions(player.pc), 1, len(player.pc)+1)
                        if swap1 is len(player.pc)+1:
                            break
                        if player.pokemon[swap1 - 1] is None:
                                clear()
                                print("You cannot select an empty slot to swap.")
                                sleep()
                                clear()
                                break
                        swap2 = getInputWithConstraints("Please selet a Pokemon to swap. ", False, getPokemonAsOptions(player.pc), 1, len(player.pc)+1)
                        if swap2 is len(player.pc)+1:
                            break
                        if player.pokemon[swap2 - 1] is None:
                                clear()
                                print("You cannot select an empty slot to swap.")
                                sleep()
                                clear()
                                break
                        if swap1 is swap2:
                            clear()
                            print("You can't swap a Pokemon with itself.")
                            sleep()
                            clear()
                            break
                        else:
                            temp = player.pokemon[swap1 - 1]
                            player.pokemon[swap1 - 1] = player.pokemon[swap2 - 1]
                            player.pokemon[swap2 - 1] = temp
                            break
                # 3. Swap pokemon in team and box
                elif opt is 3:
                    while True:
                        if len(player.pc) <= 0:
                            print("You do not have any Pokemon in your PC!")
                            sleep()
                            clear()
                            break
                        swap1 = getInputWithConstraints("Please select a Pokemon from your PC. ", False, getPokemonAsOptions(player.pc), 1, len(player.pc)+1)
                        if swap1 is len(player.pc)+1:
                            break
                        swap2 = getInputWithConstraints("Please select a Pokemon from your party to swap. ", False, getPokemonAsOptions(player.pokemon), 1, 7)
                        if swap2 is 7:
                            break
                        temp = player.pokemon[swap2 - 1]
                        player.pokemon[swap2 - 1] = player.pc[swap1 - 1]
                        player.pc[swap1 - 1] = temp
        elif usrIn is 4:
            return
        writeData("player_data.pkl", player)

def createMove():
    move = getMoveInput(1)
    if not isinstance(move, Move):
        clear()
        return
    movesDatabase.update({move.name.lower(): move})
    writeData("moves_data.pkl", movesDatabase)
    clear()

def viewPokemon():
    printPokemonWithEmptySlots(player.pokemon, False)
    input("Press enter to continue. ")
    clear()
    

def viewBackpack():
    global player
    stacks = player.backpack.stacks
    if len(stacks) > 0:
        for s in stacks:
            print(stacks.get(s))
    else:
        print("You have no items.")
    input("Press enter to continue.")
    clear()

defaultGameVolume = 1
defaultMuted = False
defaultSelectVolume = 1
defaultSettings = [defaultGameVolume, defaultMuted, defaultSelectVolume]

settings = readData("settings.pkl", defaultSettings)

gameVolume = settings[0]
muted = settings[1]
selectVolume = settings[2]

if muted:
    try:
        ss.set_volume(0.0)
    except AttributeError:
        None

def settingsEditor():
    global muted
    global gameVolume
    global selectVolume
    while True:
        options = ["1. Volume Strength", "2. Sound Effects Volume Strength", "3. Mute/Unmute Volume", "4. Back to Main Menu"]
        usrIn = getInputWithConstraints("Please select a setting. ", False, options, 1, 4)
        if usrIn is 1:
            if muted:
                print("Cannot change volume because game is muted. Please unmute in settings.")
                sleep()
                clear()
                continue
            else:
                usrIn2 = getInputWithConstraints("Please select a value between 0.0 and 1.0. (~ to exit) ", True, None, 0.0, 1.0, True)
                if usrIn2 == "~":
                    break
                gameVolume = usrIn2
                pygame.mixer.music.set_volume(gameVolume)
                settings[0] = gameVolume
                # SET OTHER EFFECTS TOO!
                writeData("settings.pkl", settings)
        elif usrIn is 2:
            if muted:
                print("Cannot change volume because game is muted. Please unmute in settings.")
                sleep()
                clear()
                continue
            else:
                usrIn2 = getInputWithConstraints("Please select a value between 0.0 and 1.0. (~ to exit) ", True, None, 0.0, 1.0, True)
                if usrIn2 == "~":
                    break
                selectVolume = usrIn2
                settings[2] = selectVolume
                try:
                    ss.set_volume(selectVolume)
                    # SET OTHER EFFECTS TOO!
                    buyItem.set_volume(selectVolume)
                    useItemSound.set_volume(selectVolume)
                    notEffective.set_volume(selectVolume)
                    normalEffective.set_volume(selectVolume)
                    superEffective.set_volume(selectVolume)
                except AttributeError:
                    None

                writeData("settings.pkl", settings)
        elif usrIn is 3:
            if muted:
                pygame.mixer.music.set_volume(gameVolume)
                try:
                    ss.set_volume(selectVolume)
                    buyItem.set_volume(selectVolume)
                    useItemSound.set_volume(selectVolume)
                    notEffective.set_volume(selectVolume)
                    normalEffective.set_volume(selectVolume)
                    superEffective.set_volume(selectVolume)
                except AttributeError:
                    None
                muted = False
                settings[1] = muted
            else:
                pygame.mixer.music.set_volume(0.0)
                try:
                    ss.set_volume(0.0)
                    buyItem.set_volume(0.0)
                    useItemSound.set_volume(0.0)
                    notEffective.set_volume(0.0)
                    normalEffective.set_volume(0.0)
                    superEffective.set_volume(0.0)
                except AttributeError:
                    None
                muted = True
                settings[1] = muted
            writeData("settings.pkl", settings)
        elif usrIn is 4:
            return

def optionNine():
    clear()
    print("Goodbye!")
    sleep()

def invalid():
    clear()
    print("That option does not exist!")
    sleep()
    clear() 

def main_menu_chooser(args, closing):
    switcher = {
        1: selectBattle,
        2: pokeShop,
        3: viewBackpack,
        4: viewPokemon,
        5: viewPokemonPC,
        6: createMove,
        7: createPokemon,
        8: settingsEditor
    }
    if args is 9:
        optionNine()
        return True
    else:
        switcher.get(args, invalid)()
        return False

def startBattle(wild):
    clear()
    print("Starting battle...")
    sleep()
    clear()
    playGame(wild)

def battleAgain(options):
    while True:
        usrIn = None
        try:
            usrIn = getTextInput("Would you like to play again? (yes/no) ")
            if usrIn.lower() == 'yes':
                wildOrNot = getInputWithConstraints("Please say if you would like to have a wild pokemon battle or a trainer battle. ", True, options, 1, 2)
                if wildOrNot is 1:
                    startBattle(True)
                else:
                    startBattle(False)

            else:
                clear()
                pygame.mixer.music.stop()
                try:
                    pygame.mixer.music.load("sounds/main_theme.wav")
                    pygame.mixer.music.play(loops=-1)
                except pygame.error:
                    None
                break
        except: TypeError

def main():
    global gameVolume
    global muted
    clear()
    print("Welcome to Pokemon!")
    player.money = 1000000
    try:
        pygame.mixer.music.load("sounds/main_theme.wav")
        pygame.mixer.music.play(loops=-1)
    except pygame.error:
        None
    
    if muted:
        pygame.mixer.music.set_volume(0.0)
    else:
        pygame.mixer.music.set_volume(gameVolume)
    time.sleep(1)
    clear()
    closing = False
    while not closing:
        options = [
        "Current Money Balance: $" + str(player.getMoney()), 
        "-----------------------------" ,
        "1. Battle", 
        "2. Shop", 
        "3. Inventory",
        "4. View Team", 
        "5. Edit your Pokemon Team", 
        "6. Create new Move", 
        "7. Create new Pokemon", 
        "8. Settings", 
        "9. Close program.", 
        "-----------------------------"
        ]
        userInput = getInputWithConstraints("Please select one of the above options. ", False, options)
        clear()
        closing = main_menu_chooser(userInput, closing)
             
earthquake = Move("Earthquake", 100, 100, "physical", ground, 10)
flamethrower = Move("Flamethrower", 90, 100, "special", fire, 15)
dragon_pulse = Move("Dragon Pulse", 85, 100, "special", dragon, 10)
rock_slide = Move("Rock Slide", 75, 90, "physical", rock, 10)
solar_beam = Move("Solar Beam", 120, 100, "special", grass, 10)
hidden_power = Move("Hidden Power", 60, 100, "special", grass, 15)
energy_ball = Move("Energy Ball", 90, 100, "special", grass, 10)

charizard = Pokemon("Charizard", 78, 84, 78, 109, 85, 100, 50, MoveSet(flamethrower, earthquake,
dragon_pulse, rock_slide), fire, flying, 31, 31,
31, 31, 31, 31, 252, 252, 252, 252, 252, 252, 1.1, "medium_slow", "something", None, False)
venusaur = Pokemon("Venusaur", 80, 82, 83, 100, 100, 80, 50, MoveSet(solar_beam, earthquake, hidden_power, energy_ball), grass, poison, 31, 31, 31, 31, 31, 31, 252, 252, 252, 252, 252, 252, 1.1,
"medium_slow", "something", None, False)

# function from Pasha, StackOverFlow
def get_nth_key(dictionary, n=0):
    if n < 0:
        n += len(dictionary)
    for i, key in enumerate(dictionary.keys()):
        if i == n:
            return key
    raise IndexError("dictionary index out of range") 

defaultMovesDatabase = {
    earthquake.name.lower(): earthquake, flamethrower.name.lower(): flamethrower, dragon_pulse.name.lower(): dragon_pulse, rock_slide.name.lower(): rock_slide, solar_beam.name.lower(): 
    solar_beam, hidden_power.name.lower(): hidden_power, energy_ball.name.lower(): energy_ball
}

defaultPokemonDatabase = {
    charizard.name.lower(): charizard, venusaur.name.lower(): venusaur
}
    
movesDatabase = readData("moves_data.pkl", defaultMovesDatabase)
pokemonDatabase = readData("pokemon_data.pkl", defaultPokemonDatabase)
writeData("moves_data.pkl", movesDatabase)
writeData("pokemon_data.pkl", pokemonDatabase)
defaultPlayer = Player([copy.deepcopy(venusaur), copy.deepcopy(charizard), None, None, None, None], Backpack({}), [])
player = readData("player_data.pkl", defaultPlayer)
writeData("player_data.pkl", player)

enemy = Player([None, None, None, None, None, None], None, None)

def randomizeEnemyTeam():
    global enemy
    for i in range(0, 6):
        cap = len(pokemonDatabase) - 1
        sel = round(random.random() * cap)
        enemy.pokemon[i] = copy.deepcopy(pokemonDatabase.get(get_nth_key(pokemonDatabase, sel)))

def getRandomPokemon():
    cap = len(pokemonDatabase) - 1
    sel = round(random.random() * cap)
    return copy.deepcopy(pokemonDatabase.get(get_nth_key(pokemonDatabase, sel)))

randomizeEnemyTeam()

enemy.setActivePokemon()

def orderDeterminer(playerPokemon, enemyPokemon):
    # Order is random if both pokemon's speed stats are identical.
    if playerPokemon.speed is enemyPokemon.speed:
        ran = random.random()
        if ran >= 0 and ran <= 0.5:
            return False
        else:
            return True
    elif playerPokemon.speed > enemyPokemon.speed:
        return True
    else:
        return False

def playerAttack(moveIndex, playerPokemon, enemyPokemon):
    
    def chooser(args):
        switcher = {
            1: playerPokemon.moves.getMove1().use,
            2: playerPokemon.moves.getMove2().use
        }

        if playerPokemon.moves.getMove3():
            switcher.update({3: playerPokemon.moves.getMove3().use})
            if playerPokemon.moves.getMove4():
                switcher.update({4: playerPokemon.moves.getMove4().use})

        return switcher.get(args)(playerPokemon, enemyPokemon, True, playerPokemon.wild)

    chooser(moveIndex)

def enemyAttack(playerPokemon, enemyPokemon):
    noMove1 = enemyPokemon.moves.move1.pp <= 0
    noMove2 = enemyPokemon.moves.move2.pp <= 0
    noMove3 = True
    noMove4 = True
    if enemyPokemon.moves.move3:
        noMove3 = enemyPokemon.moves.move3.pp <= 0
        if enemyPokemon.moves.move4:
            noMove4 = enemyPokemon.moves.move4.pp <= 0

    while True:
        rand = random.random()
        if noMove1:
            if rand >= 0 and rand < 0.25:
                continue
        if noMove2:
            if rand >= 0.25 and rand < 0.5:
                continue
        if noMove3:
            if rand >= 0.5 and rand < 0.75:
                continue
        if noMove4:
            if rand >= 0.75 and rand <= 1:
                continue
        break

        # ATTACK DETERMINATION!
        # if this doesnt work revert back to enemy.activePokemon and player.activePokemon
    if rand >= 0 and rand < 0.25:
        enemyPokemon.moves.getMove1().use(enemyPokemon, playerPokemon, False, False)
    elif rand >= 0.25 and rand < 0.5:
        enemyPokemon.moves.getMove2().use(enemyPokemon, playerPokemon, False, False)
    elif rand >= 0.5 and rand < 0.75:
        enemyPokemon.moves.getMove3().use(enemyPokemon, playerPokemon, False, False)
    elif rand >= 0.75 and rand <= 1:
        enemyPokemon.moves.getMove4().use(enemyPokemon, playerPokemon, False, False)
    else:
        print("The enemy has no moves left!")

won = False

def checkForAlivePokemon(player):
    for p in player.pokemon:
        if p:
            if p.fainted is False:
                return True
    return False

def getOptions(activePokemons, goBack):
    options = []
    i = 1
    for a in activePokemons:
        options.append(str(i) + ". " + a.name)
        i += 1
    if goBack:
        options.append(str(i) + ". Go Back")
    return options

def getActivePokemon(playerPokemon):
    activePokemons = []
    for pokemon in playerPokemon:
        if pokemon:
            activePokemons.append(pokemon)
    return activePokemons

def determineDead(playerPokemon, enemyPokemon, wild):
    # Determine if enemy pokemon is dead and out of pokemon.
    if enemyPokemon.fainted:
        if wild:
            print("The wild " + enemyPokemon.name + " fainted!" )
            sleep()
            global won
            won = True
        else: 
            print("The enemy's " + enemyPokemon.name + " fainted!")
            sleep()
            for p in enemy.pokemon:
                if p:
                    if p.fainted is False:
                        enemy.activePokemon = p
                        break
            if enemy.activePokemon.fainted:
                clear()
                print("The enemy has no more pokemon! You win!")
                player.giveMoney(500)
                writeData("player_data.pkl", player)
                won = True
            else:
                print("The enemy sent out " + enemy.activePokemon.name + "!")
                sleep()
                clear()
        return True

    # Determine if player pokemon is dead and out of pokemon.
    if player.activePokemon.fainted:
        print(player.activePokemon.name + " fainted!")
        sleep()
        clear()
        while True:
            if not checkForAlivePokemon(player):
                print("You have no more pokemon! You lose. :(")
                player.takeMoney(500)
                writeData("player_data.pkl", player)
                won = True
                break
            userInput = None
            activePokemons = getActivePokemon(player.pokemon)
            options = getOptions(activePokemons, False)
            while True:
                try:
                    userInput = getInputWithConstraints("Please select a Pokemon. ", False, options, 1, len(activePokemons))
                    break
                except ValueError:
                    print("Invalid Input!")
                    sleep()
                    clear()

            select = player.pokemon[userInput - 1]
            if select.fainted is False:
                player.activePokemon = select
                clear()
                print("Go! " + player.activePokemon.name + "!")
                sleep()
                clear()
                return True
            else:
                print("You cannot select a fainted pokemon!")
                sleep()
                clear()
        
        return False

def initializeGameMusic():
    pygame.mixer.music.stop()
    try:
        pygame.mixer.music.load("sounds/battle_music.wav")
        pygame.mixer.music.play(loops=-1)
    except pygame.error:
        None

gameCounter = 0

def playGame(wild):
    global caughtP
    caughtP = False
    global won
    won = False
    global gameCounter
    initializeGameMusic()
    resetPlayerPokemon(player)
    randomizeEnemyTeam()
    resetPlayerPokemon(enemy)
    # Is the enemy a wild pokemon or a trainer battle?
    if wild:
        enemy.activePokemon = getRandomPokemon()
        enemyActivePokemon = enemy.activePokemon
        enemyActivePokemon.wild = True
    else: 
        enemyActivePokemon = enemy.activePokemon
    if wild: print("A wild " + enemyActivePokemon.name + " appeared.")
    else: print("The enemy sends out " + enemyActivePokemon.name + ".")
    print("Go! " + player.activePokemon.name + "!")
    time.sleep(3)
    clear()
    # GAME LOOP
    while not won:
        # this is a necessary check. All the game functiosn are based off of the enemyActivePokemon variable.
        # every time the game loop runs, or the enemy pokemon dies (in trainer battle), the current active enemy
        # pokemon must be updated.
        if not wild: enemyActivePokemon = enemy.activePokemon
        pStatus = "Pokemon Status: " + player.activePokemon.name + " HP: " + str(player.activePokemon.hp) + " Status: " + player.activePokemon.healthStatus.name + " | Level: " + str(player.activePokemon.level)
        eStatus = "Enemy Pokemon Status: " + enemyActivePokemon.name + " HP: " + str(enemyActivePokemon.hp)+ " Status: " + enemyActivePokemon.healthStatus.name + " | Level: " + str(enemyActivePokemon.level)
        options = [eStatus, pStatus, "1. Fight", "2. Bag", "3. Pokemon"]
        # player chooses option
        userInput = getInputWithConstraints("What will you do? ", False, options)
        clear()

        # Refactored.
        def attackOptions():
            # Content to present to user before while loop.
            usrMoves = []
            for i in range(1, player.activePokemon.moves.size() + 1):
                if player.activePokemon.moves.getMovesInArray()[i - 1] is not None:
                    usrMoves.append(str(i) + ". " + player.activePokemon.moves.getMovesInArray()[i - 1].name + 
                    " (PP: " + str(player.activePokemon.moves.getMovesInArray()[i - 1].pp) + ")")
                else:
                    usrMoves.append(str(i) + ". None")
            i += 1
            usrMoves.append(str(i) + ". Go Back")
            # Infinite while loop until user has successful input. 
            while True:
                userInput = getInputWithConstraints("What will you do? ", False, usrMoves, 1, 5)
                if userInput is 5:
                    clear()
                    break
                elif (userInput is 3 and player.activePokemon.moves.move3 is None) or (userInput is 4 and player.activePokemon.moves.move4 is None):
                    print("You cannot select a move that is None.")
                    time.sleep(3)
                    clear()
                    continue
                else:
                    clear()
                    
                    # Paralysis, Poisoned, Badly Poisoned, Burned, Frozen, Flinch, Confused, Infatuation
                    # Player or enemy attack first.
                    orderDetermined = orderDeterminer(player.activePokemon, enemyActivePokemon)

                    if orderDetermined: 
                        playerAttack(userInput, player.activePokemon, enemyActivePokemon)
                    else:
                        enemyAttack(player.activePokemon, enemyActivePokemon)
                    # Check if player or enemy are dead. 
                    if determineDead(player.activePokemon, enemyActivePokemon, enemyActivePokemon.wild):
                        break
                    # otherwise....if the player just    attacked, let the enemy attack.
                    elif orderDetermined:
                        # check for enemy inhibitors
                        enemyAttack(player.activePokemon, enemyActivePokemon)
                    # otherwise, the player attacks.
                    else:
                        # check for player inhibitors
                        playerAttack(userInput, player.activePokemon, enemyActivePokemon)
                    if isinstance(player.activePokemon.healthStatus, Flinch):
                        # we need to add another thing for flinched. it cannot be in the same slot as 'paralysis'. 
                        # otherwise it woudl be overridden.
                        player.activePokemon.healthStatus = Normal(player.activePokemon)
                    # check who is dead again.
                    determineDead(player.activePokemon, enemyActivePokemon, enemyActivePokemon.wild)
                    # any turn by turn status effects should take place right now, regardless if a pokemon dies (unless the 
                    # pokemon with the status effect is dead)
                    break

        def bagOptions():
            breakout = False
            while not breakout:
                options = []
                i = 1
                stacks = player.backpack.stacks
                for s in stacks:
                    options.append(str(i) + ". " + str(stacks.get(s)))
                    i += 1
                
                options.append(str(i) + ". Go Back" )
                userInput = getInputWithConstraints("What will you do? ", False, options, 1, len(stacks) + 1)
                selectSound()
                if userInput == len(stacks) + 1:
                    clear()
                    breakout = True
                    continue
                else:
                    clear()
                    breakout2 = False
                    activePokemons = getActivePokemon(player.pokemon)
                    options = getOptions(activePokemons, True)

                    if isinstance(list(player.backpack.stacks.values())[userInput - 1].item, GenericPokeBall): 
                        if wild:
                            # try to catch pokemoin
                            # TODO: Implement proper pokemon catch rates. Currently hardcoded as 100.
                            # TODO: implement bonus status for status effects = increase catch rate 2 for sleep/freeze, 1.5 paralysis/poison/burn, 1 normal
                            a = (((3 * enemy.activePokemon.maxHp - 2 * enemy.activePokemon.hp) * 100 * list(player.backpack.stacks.values())[userInput - 1].item.catchRate) / (3 * enemy.activePokemon.maxHp)) * 1
                            b = 65536/(255/a)**0.1875
                            player.backpack.useItem(userInput - 1, None)
                            caught = True
                            for i in range(0, 4):
                                if random.randint(0, 65535) >= b:
                                    print("Fail")
                                    sleep()
                                    clear()
                                    caught = False
                                    break
                                else:
                                    print("Shake " + str(i+1))
                                    sleep()
                                    clear()
                            if caught:
                                print("Gotcha! " + str(enemy.activePokemon.name) + " was caught. ")
                                global caughtP
                                caughtP = True
                                sleep()
                                clear()
                                global won
                                won = True
                                breakout2 = True
                                breakout = True
                            else:
                                print("Aww! So close!")
                                sleep()
                                clear()
                                breakout2 = True
                                breakout = True
                                enemyAttack(player.activePokemon, enemyActivePokemon)
                                global gameCounter
                                gameCounter += 1 
                                if determineDead(player.activePokemon, enemyActivePokemon, enemyActivePokemon.wild):
                                    if won: break
                                clear()
                        else:
                            breakout2 = True
                            clear()
                            # TODO: update to be sassy in the future?
                            print("You can't catch a pokemon in a trainer battle!")
                            sleep()
                            clear()
                    while not breakout2:
                        userInput2 = getInputWithConstraints("Please select a pokemon for the " + list(player.backpack.stacks.values())[userInput - 1].item.name + ". ", False, options, 1, len(activePokemons) + 1)
                        if userInput2 is len(activePokemons) + 1:
                            breakout2 = True
                            break
                        selectSound()
                        select = player.pokemon[userInput2 - 1]
                        clear()
                        if (select.fainted is False and not isinstance(list(player.backpack.stacks.values())[userInput - 1], RevivalItem)) or (select.fainted is True and isinstance(list(player.backpack.stack.values())[userInput - 1], RevivalItem)):
                            player.backpack.useItem(userInput - 1, select)
                            break
                        elif select.fainted and not isinstance(list(player.backpack.stacks.values())[userInput - 1], RevivalItem):
                            print("You cannot use a healing item on a fainted pokemon!")
                            sleep()
                            clear()
                        else:
                            print("You cannot use a revive item on a pokemon that is alive!")
                            sleep()
                            clear()
                    # enemy attacks after usage of item
                    if not breakout2:
                        enemyAttack(player.activePokemon, enemyActivePokemon)
                        gameCounter += 1 
                        if determineDead(player.activePokemon, enemyActivePokemon, enemyActivePokemon.wild):
                            if won: break
                        breakout = True
                    clear()

        def switchPokemon():
            breakout = False
            while not breakout:
                try:
                    activePokemons = getActivePokemon(player.pokemon)
                    options = getOptions(activePokemons, True)
                    userInput = getInputWithConstraints("please select a Pokemon. ", False, options, 1, len(activePokemons) + 1)
                    selectSound()
                    if userInput == len(activePokemons) + 1:
                        clear()
                        break
                    else:
                        clear()
                        select = player.pokemon[userInput - 1]
                        if select.fainted is False and select is not player.activePokemon:
                            player.activePokemon = select
                            print("Go! " + player.activePokemon.name + "!")
                            sleep()
                            clear()
                            enemyAttack(player.activePokemon, enemyActivePokemon)
                            global gameCounter
                            gameCounter += 1 
                            breakout = True
                        elif select is player.activePokemon:
                            print("You cannot send out the pokemon that is currently in battle!")
                            sleep()
                            clear()
                        else:
                            print("You cannot select a fainted pokemon!")
                            sleep()
                            clear()
                except ValueError:
                    print("Invalid Input!")
                    sleep()
                    clear()

        def battlePicker(args):
            switcher = {
                1: attackOptions,
                2: bagOptions, 
                3: switchPokemon
            }

            return switcher.get(args, invalid)()

        battlePicker(userInput)
    if caughtP:
        enemy.activePokemon.wild = False
        enemy.activePokemon.active = False
        for i in range(0,6):
            if not player.pokemon[i]:
                player.pokemon[i] = enemy.activePokemon
                clear()
                print(enemy.activePokemon.name + " was put in your party.")
                sleep()
                clear()
                return
        clear()
        print(enemy.activePokemon.name + " was put in the PC.")
        player.pc.append(enemy.activePokemon)
        sleep()
        clear()

def resetPlayerPokemon(human):
    for p in human.pokemon:
        if p:
            p.hp = p.maxHp
            p.attack = p.defaultAttack
            p.defense = p.defaultDefense
            p.spAttack = p.defaultSpAttack
            p.spDefense = p.defaultSpDefense
            p.speed = p.defaultSpeed
            p.fainted = False
            p.moves.reset()
    human.activePokemon = human.pokemon[0]

if __name__ == "__main__":
    main()