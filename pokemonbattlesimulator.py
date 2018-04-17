import random
import copy
from classes import Environment, Move, Pokemon, Player, MoveSet, Backpack, FullRestore, environment
from pokemontypes import flying, poison, ground, rock, fire, grass, dragon, types, water
import os
import time
import pickle
import winsound
import sys
import pygame

clear = lambda: os.system('cls')

selectSound = lambda: winsound.PlaySound("select_sound.wav", winsound.SND_ASYNC | winsound.SND_FILENAME)

def optionOne():
    startBattle()
    battleAgain()

#TODO: add boolean for confirm
def getTextInput(message):
    while True:
        try:
            usrInput = input(message)
            selectSound()
            confirm = input("Your input is " + usrInput + ". Are you sure? (type y to continue) ")
            selectSound()
            if confirm == "y":
                return usrInput
        except ValueError:
            clear()
            print("Invalid input!")
            time.sleep(2)
            clear()

def getInputWithConstraints(message, options=None, min=None, max=None):
    while True:
        if options:
            for o in options:
                print(o)
        try:
            usrInput = int(input(message))
            selectSound()
            if min and max: 
                if usrInput < min or usrInput > max:
                    raise ValueError
            clear()
            return usrInput
        except ValueError:
            clear()
            print("Invalid input!")
            time.sleep(2)
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
                    time.sleep(2)
                    clear()
    name = getTextInput("Please enter the name of move " + str(num) + ". ")
    move = movesDatabase.get(name.lower())
    if move:
        print("This move already exists in the database.")
        time.sleep(2)
        clear()
        return move
    while True:
        pType = getTextInput("Please enter the Pokemon type of this move. ")
        if types.get(pType):
            break
        print("That isn't a valid type.")
        time.sleep(2)
        clear()
    dmgType = getTextInput("Please enter if this is a physical or special move damage type. ")
    accuracy = getInputWithConstraints("Please enter an accuracy value (10 to 100) ", 10, 100)
    damage = getInputWithConstraints("Please enter a damage value (50 to 150) ", 50, 150)
    PP = getInputWithConstraints("Please enter the power point (PP) value (5 to 50) ", 5, 50)
    return Move(name, damage, accuracy, dmgType, pType, PP)

def getMovesInput():
    move1 = getMoveInput(1)
    movesDatabase.update({move1.name: move1})
    move2 = getMoveInput(2)
    movesDatabase.update({move2.name: move2})
    move3 = getMoveInput(3)
    if move3:
        movesDatabase.update({move3.name: move3})
        move4 = getMoveInput(4)
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
            time.sleep(2)
            clear()
            continue
        usrType = types.get(usrIn.lower())
        if usrType:
            return usrType
        print("Type not recognized.")
        time.sleep(2)
        clear()

def optionTwo():
    print("TODO")
    time.sleep(2)
    clear()

def optionThree():
    clear()
    print("Create your own Pokemon here!")
    print("Pokemon made here will be saved to the file.")
    print("It is advised that you take legitimate pokemon from the original game and put them in.")
    print("Don't make ridiculously overpowered/underpowred Pokemon! Normally pokemon have base stats between 50-120.")
    print("Enemies will be randomly assigned pokemon in the save game. If you make an overpowered pokemon, then the enemy might get it!")
    time.sleep(2)
    clear()
    name = getTextInput("Please enter the name of the pokemon that you would like to create. ")
    newPokemon = pokemonDatabase.get(name.lower())
    if newPokemon:
        print("This pokemon is already in the database.")
        time.sleep(2)
        clear()
        return
    hpStat = getInputWithConstraints("Please enter the HP stat. (between 1-255) ", 1, 255)
    attackStat = getInputWithConstraints("Please enter the attack stat. (between 1-255) ", 1, 255)
    defenseStat = getInputWithConstraints("Please enter the defense stat. (between 1-255) ", 1, 255)
    spAttackStat = getInputWithConstraints("Please enter the special attack stat. (between 1-255) ", 1, 255)
    spDefenseStat = getInputWithConstraints("Please enter the special defense stat. (between 1-255) ", 1, 255)
    speedStat = getInputWithConstraints("Please enter the speed stat. (between 1-255) ", 1, 255)
    moves = getMovesInput()
    type1 = typeInput("Please enter the pokemon's primary type. ", 1)
    type2 = typeInput("Please enter the pokemon's secondary type. If it does not have one, type 'none'. ", 2)
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
    healthStatus = None
    itemHeld = None
    level = getInputWithConstraints("Please enter the level for the Pokemon. (1 to 100) ", 1, 100)
    newPokemon = Pokemon(name, hpStat, attackStat, defenseStat, spAttackStat, spDefenseStat, speedStat, level, moves, type1, type2, hpIV, 
        attackIV, defenseIV, spAttackIV, spDefenseIV, speedIV, hpEV, attackEV, defenseEV, spAttackEV, spDefenseEV, speedEV, nature, 
        growthRate, passive, healthStatus, itemHeld, False)
    pokemonDatabase.update({newPokemon.name.lower(): newPokemon})
    writeData("pokemon_data.pkl", pokemonDatabase)
    clear()


def optionFour():
    print("TODO")
    time.sleep(2)
    clear()

def optionFive():
    move = getMoveInput(1)
    movesDatabase.update({move.name.lower(): move})
    writeData("moves_data.pkl", movesDatabase)
    clear()

def optionSix():
    clear()
    print("Goodbye!")
    time.sleep(2)

def invalid():
    clear()
    print("That option does not exist!")
    time.sleep(2)
    clear()

def main_menu_chooser(args, closing):
    switcher = {
        1: optionOne,
        2: optionTwo,
        3: optionThree,
        4: optionFour,
        5: optionFive
    }
    if args is 6:
        optionSix()
        return True
    else:
        switcher.get(args, invalid)()
        return False

def startBattle():
    clear()
    print("Starting battle...")
    time.sleep(2)
    clear()
    playGame()

def battleAgain():
    while True:
        usrIn = None
        try:
            usrIn = getTextInput("Would you like to play again? (yes/no) ")
            if usrIn.lower() == 'yes':
                startBattle()
            else:
                clear()
                print("Returning to main menu...")
                time.sleep(2)
                clear()
                pygame.mixer.music.stop()
                pygame.mixer.music.load("main_theme.wav")
                pygame.mixer.music.play()
                break
        except: TypeError

def main():
    clear()
    print("Welcome to Pokemon!")
    pygame.mixer.init()
    pygame.mixer.music.load("main_theme.wav")
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.2)
    time.sleep(2)
    clear()
    closing = False
    options = ["1. Battle", "2. Buy Items", "3. Create new Pokemon", "4. Create your Pokemon Team", "5. Create new Move", "6. Close program."]
    while not closing:
        userInput = getInputWithConstraints("Please select one of the following options. ", options)
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
31, 31, 31, 31, 252, 252, 252, 252, 252, 252, 1.1, "medium_slow", "something", None, None, False)
venusaur = Pokemon("Venusaur", 80, 82, 83, 100, 100, 80, 50, MoveSet(solar_beam, earthquake, hidden_power, energy_ball), grass, poison, 31, 31, 31, 31, 31, 31, 252, 252, 252, 252, 252, 252, 1.1,
"medium_slow", "something", None, None, False)

player = Player([copy.deepcopy(venusaur), copy.deepcopy(charizard), None, None, None, None], Backpack([FullRestore(), FullRestore(), FullRestore()]))
enemy = Player([copy.deepcopy(charizard), copy.deepcopy(venusaur), None, None, None, None], None)

defaultMovesDatabase = {
    earthquake.name.lower(): earthquake, flamethrower.name.lower(): flamethrower, dragon_pulse.name.lower(): dragon_pulse, rock_slide.name.lower(): rock_slide, solar_beam.name.lower(): 
    solar_beam, hidden_power.name.lower(): hidden_power, energy_ball.name.lower(): energy_ball
}

defaultPokemonDatabase = {
    charizard.name.lower(): charizard, venusaur.name.lower(): venusaur
}

def readData(filename, defaultData):
    if not os.path.exists(filename):
        open(filename, "w")
    try:
        with open(filename, "rb") as inpuut:
            return pickle.load(inpuut)
    except EOFError:
        with open(filename, "wb") as output:
            pickle.dump(defaultData, output, pickle.HIGHEST_PROTOCOL)

def writeData(filename, data):
    with open(filename, "wb") as output:
        pickle.dump(data, output, pickle.HIGHEST_PROTOCOL)
    
movesDatabase = readData("moves_data.pkl", defaultMovesDatabase)
pokemonDatabase = readData("pokemon_data.pkl", defaultPokemonDatabase)

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
            1: playerPokemon.moves.useMove1().use,
            2: playerPokemon.moves.useMove2().use,
            3: playerPokemon.moves.useMove3().use,
            4: playerPokemon.moves.useMove4().use
        }
        return switcher.get(args)(playerPokemon, enemyPokemon, True, playerPokemon.wild)

    chooser(moveIndex)

# TODO: switch
def enemyAttack(playerPokemon, enemyPokemon):
    noMove1 = enemyPokemon.moves.move1.pp <= 0
    noMove2 = enemyPokemon.moves.move2.pp <= 0
    noMove3 = enemyPokemon.moves.move3.pp <= 0
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
    if rand >= 0 and rand < 0.25:
        enemy.activePokemon.moves.useMove1().use(enemy.activePokemon, player.activePokemon, False, False)
    elif rand >= 0.25 and rand < 0.5:
        enemy.activePokemon.moves.useMove2().use(enemy.activePokemon, player.activePokemon, False, False)
    elif rand >= 0.5 and rand < 0.75:
        enemy.activePokemon.moves.useMove3().use(enemy.activePokemon, player.activePokemon, False, False)
    elif rand >= 0.75 and rand <= 1:
        enemy.activePokemon.moves.useMove4().use(enemy.activePokemon, player.activePokemon, False, False)
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

# TODO: refactor
def determineDead(playerPokemon, enemyPokemon, wild):
    # Determine if enemy pokemon is dead and out of pokemon.
    if enemyPokemon.fainted:
        if not wild:
            print("The enemy's " + enemy.activePokemon.name + " fainted!")
        else: 
            print("The wild " + enemyPokemon.name + " fainted!" )
        time.sleep(2)
        for p in enemy.pokemon:
            if p:
                if p.fainted is False:
                    enemy.activePokemon = p
                    break
        if enemy.activePokemon.fainted:
            clear()
            print("The enemy has no more pokemon! You win!")
            global won
            won = True
        else:
            print("The enemy sent out " + enemy.activePokemon.name + "!")
            time.sleep(2)
            clear()
        return True

    # Determine if player pokemon is dead and out of pokemon.
    if player.activePokemon.fainted:
        print(player.activePokemon.name + " fainted!")
        time.sleep(2)
        clear()
        while True:
            if not checkForAlivePokemon(player):
                print("You have no more pokemon! You lose. :(")
                won = True
                break
            userInput = None
            activePokemons = getActivePokemon(player.pokemon)
            options = getOptions(activePokemons, False)
            while True:
                try:
                    userInput = getInputWithConstraints("Please select a Pokemon. ", options, 1, len(activePokemons))
                    break
                except ValueError:
                    print("Invalid Input!")
                    time.sleep(2)
                    clear()

            select = player.pokemon[userInput - 1]
            if select.fainted is False:
                player.activePokemon = select
                clear()
                print("Go! " + player.activePokemon.name + "!")
                time.sleep(2)
                clear()
                return True
            else:
                print("You cannot select a fainted pokemon!")
                time.sleep(2)
                clear()
        
        return False

#TODO: refactor
def playGame():
    pygame.mixer.music.stop()
    pygame.mixer.music.load("battle_music.wav")
    pygame.mixer.music.play()
    global won
    won = False
    resetPlayerPokemon(player)
    resetPlayerPokemon(enemy)
    print("The enemy sends out " + enemy.activePokemon.name + ".")
    print("Go! " + player.activePokemon.name + "!")
    time.sleep(3)
    clear()
    # GAME LOOP
    while not won:
        # player chooses option
        pStatus = "Pokemon Status: " + player.activePokemon.name + " HP: " + str(player.activePokemon.hp) + " | Level: " + str(player.activePokemon.level)
        eStatus = "Enemy Pokemon Status: " + enemy.activePokemon.name + " HP: " + str(enemy.activePokemon.hp)+ " | Level: " + str(enemy.activePokemon.level)
        options = [pStatus, eStatus, "1. Fight", "2. Bag", "3. Pokemon"]
        userInput = getInputWithConstraints("What will you do? ", options)
        clear()

        # refactor if possible
        def battleOption1():
            # Content to presen to user before while loop.
            m3 = True
            m4 = True
            usrMoves = []     
            usrMoves.append("1. " + player.activePokemon.moves.move1.name + " (" + "PP: " + str(player.activePokemon.moves.move1.pp) +")")
            usrMoves.append("2. " + player.activePokemon.moves.move2.name + " (" + "PP: " + str(player.activePokemon.moves.move2.pp) +")")
            if player.activePokemon.moves.move3: 
                usrMoves.append("3. "+ player.activePokemon.moves.move3.name + " (" + "PP: " + str(player.activePokemon.moves.move3.pp) +")")
            else: 
                m3 = False
                usrMoves.append("3. None")
            if player.activePokemon.moves.move4: 
                usrMoves.append("4. " + player.activePokemon.moves.move4.name + " (" + "PP: " + str(player.activePokemon.moves.move4.pp) +")")
            else:
                m4 = False 
                usrMoves.append("4. None")
            usrMoves.append("5. Go Back")
            while True:
                try:
                    userInput = getInputWithConstraints("What will you do? ", usrMoves, 1, 5)
                    if userInput is 5:
                        clear()
                        break
                    elif (userInput is 3 and not m3) or (userInput is 4 and not m4):
                        print("You cannot select a move that is None.")
                        time.sleep(3)
                        clear()
                        continue
                    else:
                        clear()
                        # If orderDeterminer returns true, the player goes first. If false, the enemy goes first. 
                        if orderDeterminer(player.activePokemon, enemy.activePokemon):
                            playerAttack(userInput, player.activePokemon, enemy.activePokemon)
                            # is enemy pokemon dead?
                            if determineDead(player.activePokemon, enemy.activePokemon, enemy.activePokemon.wild):
                                #if won: break
                                break
                            # If the enemy pokemon is not dead, it can attack.
                            else:
                                enemyAttack(player.activePokemon, enemy.activePokemon)
                                # Did the player die?
                                determineDead(player.activePokemon, enemy.activePokemon, enemy.activePokemon.wild)
                            break
                        else:
                            enemyAttack(player.activePokemon, enemy.activePokemon)
                            if determineDead(player.activePokemon, enemy.activePokemon, enemy.activePokemon.wild):
                                #if won: break
                                break
                            else:
                                playerAttack(userInput, player.activePokemon, enemy.activePokemon)
                                determineDead(player.activePokemon, enemy.activePokemon, enemy.activePokemon.wild)
                        break
                except ValueError:
                    print("Invalid input!")
                    time.sleep(2)
                    clear()

        # TODO: refactor if possible
        def battleOption2():
            breakout = False
            options = []
            items = player.backpack.getAllItems()
            i = 1
            for item in items:
                options.append(str(i) + ". " + item.name)
                i += 1
            options.append(str(i) + ". Go Back" )
            while not breakout:
                try:
                    userInput = getInputWithConstraints("What will you do? ", options, 1, len(items) + 1)
                    selectSound()
                    if userInput == len(items) + 1:
                        clear()
                        breakout = True
                        continue
                    else:
                        clear()
                        breakout2 = False
                        activePokemons = getActivePokemon(player.pokemon)
                        options = getOptions(activePokemons, True)
                        while not breakout2:
                            userInput2 = getInputWithConstraints("Please select a pokemon for the " + player.backpack.items[userInput - 1].name + ". ", options, 1, len(activePokemons) + 1)
                            selectSound()
                            select = player.pokemon[userInput2 - 1]
                            clear()
                            if select.fainted is False:
                                player.backpack.useItem(userInput - 1, select)
                                break
                            else:
                                print("You cannot select a fainted pokemon!")
                                time.sleep(2)
                                clear()
                        if not breakout2:
                            enemyAttack(player.activePokemon, enemy.activePokemon)
                            if determineDead(player.activePokemon, enemy.activePokemon, enemy.activePokemon.wild):
                                if won: break
                            breakout = True
                        clear()
                except ValueError:
                    print("Invalid input!")
                    time.sleep(2)
                    clear()

        # TODO: refactor if possible
        def battleOption3():
            breakout = False
            while not breakout:
                try:
                    activePokemons = getActivePokemon(player.pokemon)
                    options = getOptions(activePokemons, True)
                    userInput = getInputWithConstraints("please select a Pokemon. ", options, 1, len(activePokemons) + 1)
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
                            time.sleep(2)
                            clear()
                            enemyAttack(player.activePokemon, enemy.activePokemon)
                            breakout = True
                        elif select is player.activePokemon:
                            print("You cannot send out the pokemon that is currently in battle!")
                            time.sleep(2)
                            clear()
                        else:
                            print("You cannot select a fainted pokemon!")
                            time.sleep(2)
                            clear()
                except ValueError:
                    print("Invalid Input!")
                    time.sleep(2)
                    clear()

        def battlePicker(args):
            switcher = {
                1: battleOption1,
                2: battleOption2, 
                3: battleOption3
            }

            return switcher.get(args, invalid)()

        battlePicker(userInput)
           
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

if __name__ == "__main__":
    main()