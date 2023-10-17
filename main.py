"""This module is used to run a human vs human game of boku"""
from random import choice

from bokuboard import bokudata
from bokuboard.bokulogic import BokuGame
from minmax.bokuagent import BokuAgent, RandomAgent, HumanAgent, HeuristicAgent

def start_game():
    """This methods starts a game of boku"""
    # initialize game
    game_on = True
    game = BokuGame()

    # set promt cycle
    promt_cycle = int(input("how many turns between prompts (1 or more)? "))# TODO command on human turn, new module?

    players = [get_player_agent("white"), get_player_agent("black")]

    #starting board (for testing purposes)
    first_move = choice(list(bokudata.all_coords))
    game.place_tile(first_move, "white")

    second_move = choice(list(bokudata.all_coords - {first_move}))
    game.place_tile(second_move, "black")


    #Play the game
    last_turn = -1
    while game_on:
    # check player to play
        turn = len(game.history) // 2
        if last_turn != turn:
            last_turn = turn
            game_balance = game.heuristic["white"].total() - game.heuristic["black"].total()
            print(f"\nturn: {turn},  game balance: {round(game_balance, 3)} ")
            print(f"{len(game.heuristic['move order'])} moves in move order priority queue")

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
        "history" : lambda: print([[game.coord_to_notation(coord) for coord in action]\
                                    for action in game.history]),
        "occupied": lambda: print(game.occupied_dict),
        "heuristic": lambda: print(game.heuristic[input("enter color: ")]),
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

    agent_dict = {
        "human" : HumanAgent,
        "random" : RandomAgent,
        "heuristic" : HeuristicAgent,
    }

    agent_list = list(agent_dict.keys())

    agent = None
    agent_choice = ""

    while agent_choice not in  agent_dict:
        agent_choice = input(f"Available agents are: {str(agent_list)}. \nwhat agent is {color.upper()}? ")
        agent = agent_dict[agent_choice](color)

    return agent



if __name__ == "__main__":
    start_game()
