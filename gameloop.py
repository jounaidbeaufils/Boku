from bokudisplay import draw_board
from bokulogic import BokuGame

def start_game():
    game_on = True
    game = BokuGame()

    #black_ai_question = input("Is black an AI? (y/n)")
    #white_ai_question = input("Is white am AI? (y/n)")

    while game_on:
        for player in ["white", "black"]:
            illegal_move = True
            while  illegal_move and game_on:
                tile = input(f"which tile does {player} place? ")
                tile_coord = BokuGame.notation_to_coord(tile)
                win, capture_choice, illegal_move = game.place_tile(tile_coord, player)
                print(win)
                
                if win:
                    print(f"{player} has won the game!")
                    game_on = False
                    break

                if capture_choice:
                    illegal_capture = True
                    while illegal_capture:
                     capture = input(f"which tile does {player} capture from the following list?\
                                     \n {BokuGame.coord_to_notation(capture_choice)}")
                     if BokuGame.notation_to_coord(capture_choice) in capture_choice:
                         illegal_capture =False
                         game.capture_tile(capture_choice)


        
        draw_board(game.occupied_list)

if __name__ == "__main__":
    start_game()
