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

    for color in ["white" , "black"]:
        print(f"capture heuristic for {color}")
        capture_choice, values = game.capture_check(user_tile, color)
        if capture_choice:
            print(capture_choice)
            break

        for key, value in values.items():
            print(f"{game.coord_to_notation(key)} : {value}")
        
        print()

    game.draw_board()
