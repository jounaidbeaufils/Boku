""" use "/usr/bin/python3 -m tests.test_win_heuristic" to run this file
"""
from bokulogic import BokuGame

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

    win, values = game.win_check(user_tile, user_player)
    if win:
        print("player win!")
        break

    for key, value in values.items():
        print(f"{game.coord_to_notation(key)} : {value}")

    game.draw_board()
