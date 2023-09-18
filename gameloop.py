from bokulogic import BokuGame

def start_game():
    game_on = True
    game = BokuGame()

    #starting board (for testing)
    white_tiles = ["g3"]
    black_tiles = ["g4","g5"]

    for notation in white_tiles:
        game.place_tile(BokuGame.notation_to_coord(notation), "white")
    
    for notation in black_tiles:
        game.place_tile(BokuGame.notation_to_coord(notation), "black")

    #Play the game
    while game_on:
        for player in ["white", "black"]:
            illegal_move = True
            while  illegal_move and game_on:
                tile = input(f"which tile does {player} place? ")
                tile_coord = BokuGame.notation_to_coord(tile)
                win, capture_choice, illegal_move = game.place_tile(tile_coord, player)

                if win:
                    print(f"{player} has won the game!")
                    game_on = False
                    break

                if capture_choice:
                    illegal_capture = True
                    while illegal_capture:
                     notation_list = [BokuGame.coord_to_notation(x, y, z) for x,y,z in capture_choice]
                     game.draw_board()
                     capture = input(f"which tile does {player} capture from the following list {notation_list}? ")
                     if BokuGame.notation_to_coord(capture) in capture_choice:
                         illegal_capture =False
                         game.capture_tile(BokuGame.notation_to_coord(capture))
        print()
        
        game.draw_board()

    restart = input("do you want to play another game (y/n)? ")
    if restart == "y":
        start_game()

if __name__ == "__main__":
    start_game()
