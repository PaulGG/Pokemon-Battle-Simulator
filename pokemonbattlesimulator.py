import random
import copy
from classes import Environment, Move, Pokemon, Player, MoveSet, Backpack, FullRestore, environment
from pokemontypes import flying, poison, ground, rock, fire, grass, dragon


def main():
    print("Welcome to Pokemon!")
    print("Starting battle...")
    playGame()
    while True:
        usrIn = None
        try:
            usrIn = input("Would you like to play again? (yes/no) ")
            if usrIn.lower() == 'yes':
                playGame()
            else:
                print("Goodbye!")
                break
        except: TypeError

# Adding two pokemon to test everything.

earthquake = Move("Earthquake", 100, 100, "physical", ground, 10)
charizard = Pokemon("Charizard", 78, 84, 78, 109, 85, 100, 50, MoveSet(Move("Flamethrower", 90, 100, "special", fire, 15), earthquake,
Move("Dragon Pulse", 85, 100, "special", dragon, 10), Move("Rock Slide", 75, 90, "physical", rock, 10)), fire, flying, 31, 31,
31, 31, 31, 31, 252, 252, 252, 252, 252, 252, 1.1, "medium_slow", "something", None, None)
venusaur = Pokemon("Venusaur", 80, 82, 83, 100, 100, 80, 50, MoveSet(Move("Solar Beam", 120, 100, "special", grass, 10), earthquake, Move("Hidden Power",
60, 100, "special", grass, 15), Move("Energy Ball", 90, 100, "special", grass, 10)), grass, poison, 31, 31, 31, 31, 31, 31, 252, 252, 252, 252, 252, 252, 1.1,
"medium_slow", "something", None, None)


player = Player([copy.deepcopy(venusaur), copy.deepcopy(charizard), None, None, None, None], Backpack([FullRestore(), FullRestore(), FullRestore()]))
enemy = Player([copy.deepcopy(charizard), copy.deepcopy(venusaur), None, None, None, None], None)

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
    if moveIndex is 1:
        playerPokemon.moves.useMove1().use(playerPokemon, enemyPokemon, True)
    elif moveIndex is 2:
        playerPokemon.moves.useMove2().use(playerPokemon, enemyPokemon, True)
    elif moveIndex is 3:
        playerPokemon.moves.useMove3().use(playerPokemon, enemyPokemon, True)
    else:
        playerPokemon.moves.useMove4().use(playerPokemon, enemyPokemon, True)


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
        enemy.activePokemon.moves.useMove1().use(enemy.activePokemon, player.activePokemon, False)
    elif rand >= 0.25 and rand < 0.5:
        enemy.activePokemon.moves.useMove2().use(enemy.activePokemon, player.activePokemon, False)
    elif rand >= 0.5 and rand < 0.75:
        enemy.activePokemon.moves.useMove3().use(enemy.activePokemon, player.activePokemon, False)
    elif rand >= 0.75 and rand <= 1:
        enemy.activePokemon.moves.useMove4().use(enemy.activePokemon, player.activePokemon, False)
    else:
        print("The enemy has no moves left!")

won = False

def checkForAlivePokemon(player):
    for p in player.pokemon:
        if p:
            if p.fainted is False:
                return True
    return False

def determineDead(playerPokemon, enemyPokemon):
    if enemyPokemon.fainted:
        print("The enemy's " + enemy.activePokemon.name + " fainted!")
        for p in enemy.pokemon:
            if p:
                if p.fainted is False:
                    enemy.activePokemon = p
                    break
        # TODO: BETTER ENDGAME
        if enemy.activePokemon.fainted:
            print("The enemy has no more pokemon! You win!")
            global won
            won = True
        else:
            print("The enemy sent out " + enemy.activePokemon.name + "!")
        return True

    if player.activePokemon.fainted:
        print(player.activePokemon.name + " fainted!")
        while True:
            if not checkForAlivePokemon(player):
                print("You have no more pokemon! You lose. :(")
                won = True
                break
            i = 1
            activePokemons = []
            for pokemon in player.pokemon:
                if pokemon:
                    activePokemons.append(pokemon)
                    print(str(i) + ". " + pokemon.name)
                    i += 1
            userInput = None
            while True:
                try:
                    userInput = int(input("Please select a Pokemon. "))
                    if userInput > len(activePokemons): print("That selection does not exist!")
                    else: break
                except ValueError:
                    print("Invalid Input!")

            select = player.pokemon[userInput - 1]
            if select.fainted is False:
                player.activePokemon = select
                print("Go! " + player.activePokemon.name + "!")
                return True
            else:
                print("You cannot select a fainted pokemon!")

def playGame():
    global won
    won = False
    resetPlayerPokemon(player)
    resetPlayerPokemon(enemy)

    print("The enemy sends out " + enemy.activePokemon.name + ".")
    print("Go! " + player.activePokemon.name + "!")
    # GAME LOOP
    while not won:
        # player chooses option
        print("Pokemon Status: " + player.activePokemon.name + " HP: " + str(player.activePokemon.hp) + " | Level: " + str(player.activePokemon.level))
        print("Enemy Pokemon Status: " + enemy.activePokemon.name + " HP: " + str(enemy.activePokemon.hp)+ " | Level: " + str(enemy.activePokemon.level))
        print("1. Fight")
        print("2. Bag")
        print("3. Pokemon")
        while True:
            try:
                userInput = int(input("What will you do? "))
                break
            except ValueError:
                print("Invalid input!")

        m1 = True
        m2 = True
        m3 = True
        m4 = True

        if userInput is 1:
            if player.activePokemon.moves.move1:     
                print("1. " + player.activePokemon.moves.move1.name + " (" + "PP: " + str(player.activePokemon.moves.move1.pp) +")")
            else: 
                m1 = False
                print("1. None")
            if player.activePokemon.moves.move2: 
                print("2. " + player.activePokemon.moves.move2.name + " (" + "PP: " + str(player.activePokemon.moves.move2.pp) +")")
            else: 
                m2 = False
                print("2. None")
            if player.activePokemon.moves.move3: 
                print("3. "+ player.activePokemon.moves.move3.name + " (" + "PP: " + str(player.activePokemon.moves.move3.pp) +")")
            else: 
                m3 = False
                print("3. None")
            if player.activePokemon.moves.move4: 
                print("4. " + player.activePokemon.moves.move4.name + " (" + "PP: " + str(player.activePokemon.moves.move4.pp) +")")
            else:
                m4 = False 
                print("4. None")
            print("5. Go Back")
            userInput = int(input("What will you do? "))
            # ATTACK DETERMINATION!
            if userInput not in [1, 2, 3, 4]:
                continue
            elif (userInput is 1 and not m1) or (userInput is 2 and not m2) or (userInput is 3 and not m3) or (userInput is 4 and not m4):
                print("You cannot select a move that is None.")
                continue
            else:
                if orderDeterminer(player.activePokemon, enemy.activePokemon):
                    playerAttack(userInput, player.activePokemon, enemy.activePokemon)
                    # is enemy pokemon dead?
                    if determineDead(player.activePokemon, enemy.activePokemon):
                        if won: break
                        continue

                    else:
                        enemyAttack(player.activePokemon, enemy.activePokemon)
                        if determineDead(player.activePokemon, enemy.activePokemon):
                            if won: break
                else:
                    enemyAttack(player.activePokemon, enemy.activePokemon)
                    if determineDead(player.activePokemon, enemy.activePokemon):
                        if won: break
                    else:
                        playerAttack(userInput, player.activePokemon, enemy.activePokemon)
                        if determineDead(player.activePokemon, enemy.activePokemon):
                            if won: break
        elif userInput is 2:
            if player.backpack:
                items = player.backpack.getAllItems()
                i = 1
                for item in items:
                    print(str(i) + ". " + item.name)
                    i += 1
                print(str(i) + ". Go Back" )
                userInput = None
                while True:
                    try:
                        userInput = int(input("What will you do? "))
                        break
                    except ValueError:
                        print("Invalid input!")
                if userInput > len(items) or userInput < 1:
                    # go back
                    continue
                else:
                    while True:
                        j = 1
                        activePokemons = []
                        for pokemon in player.pokemon:
                            if pokemon:
                                activePokemons.append(pokemon)
                                print(str(j) + ". " + pokemon.name)
                                j += 1
                        userInput2 = int(input("Please select a pokemon for that item. "))
                        select = player.pokemon[userInput2 - 1]
                        if select.fainted is False:
                            player.backpack.useItem(userInput - 1, select)
                            break
                        else:
                            print("You cannot select a fainted pokemon!")
                    enemyAttack(player.activePokemon, enemy.activePokemon)
                    if determineDead(player.activePokemon, enemy.activePokemon):
                        if won: break

        elif userInput is 3:
            i = 1
            activePokemons = []
            for pokemon in player.pokemon:
                if pokemon:
                    activePokemons.append(pokemon)
                    print(str(i) + ". " + pokemon.name)
                    i += 1
            print(str(i) + ". Go Back")
            while True:
                try:
                    userInput = int(input("Please select a Pokemon. "))
                    break
                except ValueError:
                    print("Invalid Input!")
            if userInput == i:
                continue
            elif userInput > len(activePokemons) or userInput < 1:
                continue
            else:
                select = player.pokemon[userInput - 1]
                if select.fainted is False:
                    player.activePokemon = select
                    print("Go! " + player.activePokemon.name + "!")
                    enemyAttack(player.activePokemon, enemy.activePokemon)
                #TODO fix this garbage so that it tells the user to repick the pokemon. this requires functions which too lazy to do right now
                else:
                    print("You cannot select a fainted pokemon!")
        else:
            print("That option does not exist!")

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


main()