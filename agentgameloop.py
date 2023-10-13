"""This module is used to run a human vs human game of boku"""
from bokulogic import BokuGame
from bokuagent import BokuAgent, RandomAgent, HumanAgent

def start_game():
    """This methods starts a game of boku"""
    # initialize game
    game_on = True
    game = BokuGame()

    # set promt cycle
    promt_cycle = int(input("how many turns between prompts (1 or more)? "))#TODO at first command on human turn, new module?

    players = [get_player_agent("white"), get_player_agent("black")]

    #starting board (for testing purposes)
    for notation in []:
        game.place_tile(game.notation_to_coord(notation), "white")

    for notation in []:
        game.place_tile(game.notation_to_coord(notation), "black")

    #Play the game
    last_turn = -1
    while game_on:
    # check player to play
        turn = len(game.history) // 2
        if last_turn != turn:
            last_turn = turn
            print(f"\nturn {turn}")

        player = players[len(game.history) % 2]
        move = player.play(game)

        # TODO  update how wins are checked
        win, _ = game.win_check(move, player.color)
        if win:
            print(f"{player.color} has won the game!")
            game_on = False
            run_command("display", game)

        if (turn + 1) % promt_cycle == 0 and player.color == "black":
            command = "start"
            while command != "":
                command = input("press enter to continue or type a command: ")
                if command != "":
                    run_command(command, game)
        
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
        "occupied": lambda: print(game.occupied_dict),
        "heuristic" : lambda: print([(game.coord_to_notation(coord), value) for coord, value in game.heuristic["win"].items()]),
        "capture heuristic" : lambda: print([(game.coord_to_notation(coord), value) for coord, value in game.heuristic["capture"].items()]),
    }
    if command not in command_dict:
        print(f"command '{command}' is not a valid command")

    else:
        # run command
        data = command_dict[command]()

        # print command data
        print_list = []
        if command in print_list:
            print(data)

def get_player_agent(color) -> BokuAgent:
    """This function asks the user if the player is an AI and returns the corresponding agent"""

    is_ai = ""
    agent = None
    while is_ai != "y" and is_ai != "n":
        is_ai = input("is player an AI (y/n)? ")

    if is_ai == "y":
        agent = RandomAgent(color)
    else:
        agent = HumanAgent(color)

    return agent



if __name__ == "__main__":
    start_game()
