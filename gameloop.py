"""This module is used to run a human vs human game of boku"""
from bokulogic import BokuGame

def start_game():
    """This methods starts a game of boku"""
    game_on = True
    game = BokuGame()

    #starting board (for testing purposes)
    for notation in []:
        game.place_tile(game.notation_to_coord(notation), "white")

    for notation in []:
        game.place_tile(game.notation_to_coord(notation), "black")

    #Play the game
    last_turn = 0
    while game_on:
        # check player to play
        player = "white" if len(game.history) % 2 == 0 else "black"
        turn = len(game.history) // 2
        if last_turn != turn:
            last_turn = turn
            print()

        # input tile
        tile_notation = input(f"turn {turn}, which tile does {player} place? ")

        # check for commands and run them
        if tile_notation != "" and tile_notation[0] == "\\":
            run_command(tile_notation[1:], game)
            continue

        # translate notation
        tile_coord = game.notation_to_coord(tile_notation)

        # avoid invalid tile notations
        if tile_coord == (-99, -99, -99):
            print(f"the tile '{tile_notation}' does not exist")
            continue

        win, capture_choice, illegal_move = game.place_tile(tile_coord, player)

        if illegal_move:
            print(f"move '{tile_notation}' is not allowed")

        if win:
            print(f"{player} has won the game!")
            game_on = False
            break

        if capture_choice:
            illegal_capture = True
            while illegal_capture:
                notation_list = [game.coord_to_notation(coord) for coord in capture_choice]
                capture = input(f"which tile does {player} capture from the following list {notation_list}? ")
                capture = game.notation_to_coord(capture)
                if capture in capture_choice:
                    illegal_capture =False
                    game.capture_tile(capture)

    restart = input("do you want to play another game (y/n)? ")
    if restart == "y":
        start_game()

def run_command(command: str, game: BokuGame):
    """this fuction is used to execute commands while the game loop is rnning"""
    command_dict = {
        "undo" : game.undo,
        "display" : game.draw_board,
        # i don't want to declare a wrapper function
        # this list comprehension converts from coordinates to notation
        "history" : lambda: print([[game.coord_to_notation(coord) for coord in action] for action in game.history]),
        "occupied": lambda: print(game.occupied_dict)
    }
    if command not in command_dict:
        print(f"command '\\{command}' is not a valid command")

    else:
        # run command
        data = command_dict[command]()

        # print command data
        print_list = []
        if command in print_list:
            print(data)

if __name__ == "__main__":
    start_game()
