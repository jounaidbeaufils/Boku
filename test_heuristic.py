from bokulogic import BokuGame

game = BokuGame()

while True:
    user_input = input()
    user_input = game.notation_to_coord(user_input)
    if user_input == (-99,-99,-99):
        print("tile does not exist")
        continue 

    result = game.place_tile(user_input, "white")
    print(not result)

    win, values = game.win_check(user_input)
    if win:
        print("player win!")
        break
    
    for key, value in values.items():
        print(f"{game.coord_to_notation(key)} : {value}")

    game.draw_board()
