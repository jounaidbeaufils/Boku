"""This module is used to run a human vs human game of boku"""
from random import choice

from bokuboard import bokudata
from bokuboard.bokulogic import BokuGame
from bokuboard.bokudata import coord_to_notation
from minmax.bokuagent import BokuAgent
from userinputs.inputgetters import get_player_agent, get_int, get_y_or_n
from userinputs.commands import run_command

def play_x_games(x=None, white: BokuAgent=None, black: BokuAgent=None,
                 promt_cycle=None, random_start=None):
    """plays x games of boku"""
    if x is None:
        x = get_int("how many games? ", 1, 1000000)

    if promt_cycle is None:
        promt_cycle = get_int("how many turns between prompts (1 or more)? ", 1, 1000000)

    if white is None:
        white = get_player_agent("white")

    if black is None:
        black = get_player_agent("black")

    players = [white, black]

    if random_start is None:
        random_start = get_y_or_n("random start? (y/n) ")

    game_log = {"white win" : 0,
                "black win" : 0,
                "draw" : 0,
                "black suprise win" : 0,
                "white suprise win" : 0}

    for i in range(int(x)):
        print(f"\nStarting game {i}")
        start_game(i, players=players, promt_cycle=promt_cycle,
                   game_log=game_log, random_start=random_start)

    print(f"{game_log}")

def start_game(game_n, players, promt_cycle, game_log, random_start):
    """This methods starts a game of boku"""

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

if __name__ == "__main__":
    play_x_games()
