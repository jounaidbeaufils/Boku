""" use "/usr/bin/python3 -m tests.test_win_heuristic" to run this file
"""
from bokuboard.bokulogic import BokuGame
from bokuboard.bokudata import coord_to_notation, notation_to_coord
from bokuboard.bokudisplay import draw_board

game = BokuGame()

while True:
    user_player = input("player to play: ")
    user_tile = input("tile to play: ")
    user_tile = notation_to_coord(user_tile)
    if user_tile == (-99,-99,-99):
        print("tile does not exist")
        continue 

    result = game._place_tile(user_tile, user_player)
    print(not result)

    win, values = game._win_check(user_tile, user_player)
    if win:
        print("player win!")
        break

    for key, value in values.items():
        print(f"{coord_to_notation(key)} : {value}")

    draw_board(game)
