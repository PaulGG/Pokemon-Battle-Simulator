def optionFour():
    clear()
    # print user current team
    while True:
        print("Here are the pokemon currently on your team: ")
        printPokemonWithEmptySlots(player.pokemon, False)
        strIn = getTextInput("Please enter a pokemon that you would like on your team. (~ to exit) ")
        if strIn == "~": 
            clear()
            break
        # search database
        clear()
        usrSelect = pokemonDatabase.get(strIn.lower(), None)
        if usrSelect:
            printPokemonWithEmptySlots(player.pokemon, True)
            counter = 1
            for p in player.pokemon:
                if p:
                    counter += 1
            intIn = getInputWithConstraints("Which pokemon would you like to replace? (~ to exit) ", True, None, 1, counter)
            if intIn == "~":
                clear()
                break
            player.pokemon[intIn - 1] = copy.deepcopy(usrSelect)
            player.setActivePokemon()
            writeData("player_data.pkl", player)
            return
        else:
            print("That pokemon was not found in the database.")
            sleep()
            clear()
    writeData("player_data.pkl", player)