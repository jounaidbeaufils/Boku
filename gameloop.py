from bokudisplay import draw_board
from bokulogic import BokuGame

def start_game():
    game_on = True
    game = BokuGame()

    #black_ai_question = input("Is black an AI? (y/n)")
    #white_ai_question = input("Is white am AI? (y/n)")

    while game_on:
        for player in ["white", "black"]:
            illegal = True
            while illegal:
                tile = input(f"which tile does {player} place?")
                tile_coord = BokuGame.notation_to_coord(tile)
                _, _, illegal = game.place_tile(tile_coord, player)
        
        draw_board(game.occupied_list)

if __name__ == "__main__":
    start_game()
