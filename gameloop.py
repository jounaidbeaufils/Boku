from bokulogic import BokuGame

def start_game():
    game_on = True
    game = BokuGame()

    #starting board (for testing)
    white_tiles = []
    black_tiles = []

    for notation in white_tiles:
        game.place_tile(BokuGame.notation_to_coord(notation), "white")
    
    for notation in black_tiles:
        game.place_tile(BokuGame.notation_to_coord(notation), "black")

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
        tile = input(f"turn {turn}, which tile does {player} place? ")

        # check for commands and run them
        if tile[0] == "\\":
            run_command(tile[1:], game)
            continue

        elif tile.upper() not in game.valid_notation:
            print(f"the tile {tile} is does not exist on the board")
            continue

        else:
            tile = BokuGame.notation_to_coord(tile)
            win, capture_choice, illegal_move = game.place_tile(tile, player)

        if illegal_move:
            print("move not allowed")

        if win:
            print(f"{player} has won the game!")
            game_on = False
            break

        if capture_choice:
            illegal_capture = True
            while illegal_capture:
                notation_list = [BokuGame.coord_to_notation(x, y, z) for x,y,z in capture_choice]
                capture = input(f"which tile does {player} capture from the following list {notation_list}? ")
                capture = BokuGame.notation_to_coord(capture)
                if capture in capture_choice:
                    illegal_capture =False
                    game.capture_tile(capture)
        
    restart = input("do you want to play another game (y/n)? ")
    if restart == "y":
        start_game()

def run_command(command, game):
    command_dict = {
        "undo" : game.undo,
        "display" : game.draw_board
    }
    if command not in command_dict.keys():
        print(f"command '{command}' is not a valid command")
    else:
        command_dict[command]()

if __name__ == "__main__":
    start_game()
