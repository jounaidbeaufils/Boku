""""this file contains functions that are used to debug the game"""
from bokuboard.bokulogic import BokuGame
from bokuboard.bokudata import coord_to_notation
from bokuboard.bokudisplay import draw_board

def run_command(command: str, game: BokuGame):
    """this fuction is used to execute commands while the game loop is rnning"""
    if command == "start":
        while command != "":
            command = input("press enter to continue or type a command: ")
            if command != "":
                run_command(command, game)
    else:
        command_dict = {
            "undo" : game.undo,
            "display" : lambda: draw_board(game),
            # i don't want to declare a wrapper function
            # this list comprehension converts from coordinates to notation
            "history" : lambda: print([[coord_to_notation(coord) for coord in action]\
                                        for action in game.history]),
            "occupied": lambda: print({coord_to_notation(coord) : value 
                                       for coord, value in game.occupied_dict.items()}),
            "heuristic": lambda: print({coord_to_notation(coord): round(value, 3)
                                        for coord, value in game.heuristic[
                                            input("enter color: ")].items()}),
            "undo tracker": lambda: print(game.heuristic_undo_tracker),
            "no play": lambda: print(coord_to_notation(game.no_play_tile)),
            "best move": lambda: print([coord_to_notation(elm.tile) +
                                        f": {str(round(elm.value, 3))}"
                                        for elm in game.heuristic["move order"]]),
        }
        if command not in command_dict:
            print(f"command '{command}' is not a valid command")

        else:
            # run command
            data = command_dict[command]()

            # print command data
            print_list = []
            if command in print_list:
                print(data)
