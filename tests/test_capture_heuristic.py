""" use "/usr/bin/python3 -m tests.test_capture_heuristic" to run this file
"""
from bokuboard.bokulogic import BokuGame

game = BokuGame()

while True:
    user_player = input("player to play: ")
    user_tile = input("tile to play: ")
    user_tile = game.notation_to_coord(user_tile)
    if user_tile == (-99,-99,-99):
        print("tile does not exist")
        continue 

    result = game.place_tile(user_tile, user_player)
    print(not result)

    for color in ["white", "black"]:
        print(f"capture heuristic for {color}")
        capture_choice, values = game._capture_check(user_tile, color)
        print(f"capture_choice: {[game.coord_to_notation(x) for x in capture_choice]}")

        for key, value in values.items():
            print(f"{game.coord_to_notation(key)} : {value}")
        
        print()

    game.draw_board()
