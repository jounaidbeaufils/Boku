"""This module is used to run a human vs human game of boku"""
from random import choice

from bokuboard import bokudata
from bokuboard.bokulogic import BokuGame
from bokuboard.bokudata import coord_to_notation
from minmax.bokuagent import (BokuAgent, RandomAgent, HumanAgent, HeuristicAgent,
                             ABNMAgentRandomCapture)

# TODO sanitize all inputs and prevent a crash from bad input

def play_x_games(x=None, white=None, black=None, promt_cycle=None, random_start=None):
    """plays x games of boku"""
    if x is None:
        x = int(input("how many games do you want to play? "))

    game_log = {"white win" : 0,
                "black win" : 0,
                "draw" : 0,
                "black suprise win" : 0,
                "white suprise win" : 0}

    for i in range(int(x)):
        print(f"\nStarting game {i}")
        start_game(i, white=white, black=black, promt_cycle=promt_cycle,
                   game_log=game_log, random_start=random_start)

    print(f"{game_log}")

def start_game(game_n, white=None, black=None, promt_cycle=None, game_log=None, random_start=None):
    """This methods starts a game of boku"""

    # set promt cycle
    if promt_cycle is None:
        # TODO command on human turn, new module?
        promt_cycle = int(input("how many turns between prompts (1 or more)? "))

    # set players
    players = [get_player_agent("white") if white is None else agent_dict[white]("white"),
               get_player_agent("black") if black is None else agent_dict[black]("black")]

    # initialize game
    game_on = True
    game = BokuGame()

    #starting board (for testing purposes)
    if random_start:
        first_move = choice(list(bokudata.all_coords))
        game.play_tile(first_move, "white")

        second_move = choice(list(bokudata.all_coords - {first_move}))
        game.play_tile(second_move, "black")

    # pleyers out of options
    white_out = False
    black_out = False

    #Play the game
    last_turn = -1
    while game_on:
    # check player to play
        turn = len(game.history) // 2
        if last_turn != turn:
            last_turn = turn
            game_balance = game.eval()
            print(f"\ngame: {game_n}, turn: {turn},  game balance: {game_balance} ")

        player = players[len(game.history) % 2]
        win, move = player.play(game)

        # check if player is out of options
        if move is None and player.color == "white":
            print("white has no legal moves")
            white_out = True
        elif move is None and player.color == "black":
            print("black has no legal moves")
            black_out = True

        else:
            #TODO print capture move correctly, read history
            print(f"{player.color} plays {coord_to_notation(move)}")

        # check if the playing player has won
        if win:
            print(f"{player.color} has won the game!")
            game_on = False
            suprise = game_balance > 0 and player.color == "black"\
                    or game_balance < 0 and player.color == "white"
            game_log[f"{player.color} {'suprise ' if suprise else ''}win"] += 1

        # check if the game is a draw
        if white_out and black_out:
            print("the game is a draw")
            game_on = False
            game_log["draw"] += 1

        # run command opportunity at interval
        if ((turn + 1) % promt_cycle == 0 and player.color == "black") or not game_on:
            run_command("start", game)

def run_command(command: str, game: BokuGame):
    """this fuction is used to execute commands while the game loop is rnning"""
    if command == "start":
        while command != "":
            command = input("press enter to continue or type a command: ")
            if command != "":
                run_command(command, game)
    else:
        command_dict = {
            "undo" : game.undo,
            "display" : game.draw_board,
            # i don't want to declare a wrapper function
            # this list comprehension converts from coordinates to notation
            "history" : lambda: print([[coord_to_notation(coord) for coord in action]\
                                        for action in game.history]),
            "occupied": lambda: print(game.occupied_dict),
            "heuristic": lambda: print(game.heuristic[input("enter color: ")]),
            "undo tracker": lambda: print(game.heuristic_undo_tracker),
            "no play": lambda: print(coord_to_notation(game.no_play_tile)),
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

agent_dict = {
        "human" : HumanAgent,
        "random" : RandomAgent,
        "heuristic" : HeuristicAgent,
        "abnm" : ABNMAgentRandomCapture,
    }

def get_player_agent(color) -> BokuAgent:
    """This function asks the user if the player is an AI and returns the corresponding agent"""
    agent_list = list(agent_dict.keys())

    agent = None
    agent_choice = ""

    while agent_choice not in  agent_dict:
        agent_choice = input(f"""Available agents are: {str(agent_list)}.
                                 what agent is {color.upper()}? """)
        agent = agent_dict[agent_choice](color)

    return agent



if __name__ == "__main__":
    white_agent = input("white agent: ")
    black_agent = input("black agent: ")
    random_start_input = input("random start? (y/n) ").lower() == "y"
    promt_cycle_input = int(input("how many turns between prompts (1 or more)? "))
    games_number = int(input("how many games? "))

    play_x_games(games_number, white_agent, black_agent, promt_cycle_input, random_start_input)
