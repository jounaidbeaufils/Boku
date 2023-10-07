"""Module for all Boku agents."""
from abc import ABC, abstractmethod
from bokulogic import BokuGame
from random import randint

class BokuAgent(ABC):
    """Abstract base class for all Boku agents."""
    def __init__(self, color: str):
        self.color = color

    @abstractmethod
    def play(self, game: BokuGame):
        """Play a move."""

    def turn_to_play(self, game: BokuGame):
        """Return the player and turn to play."""        
        player = "white" if len(game.history) % 2 == 0 else "black"
        turn = len(game.history) // 2
        return turn, player

class RandomAgent(BokuAgent):
    """Agent plays random player."""
    def play(self, game: BokuGame):
        """Play a move."""
        # get all valid moves
        valid_moves = [move for move in game.occupied_dict if game.occupied_dict[move] == "free" and move != game.no_play_tile]

        # choose a random move
        move_index = randint(0, len(valid_moves) - 1)

        # play the move
        game.place_tile(valid_moves[move_index], self.color)
        print(f"{self.color} RandomAgent plays {game.coord_to_notation(valid_moves[move_index])}")

        # capture if possible
        capture_choice, _ = game.capture_check(valid_moves[move_index], self.color)
        if capture_choice:
            capture_index = randint(0, len(capture_choice) - 1)
            game.capture_tile(capture_choice[capture_index])


class HumanAgent(BokuAgent):
    """Class for human players."""
    def play(self, game: BokuGame):
        """Play a move by asking the user for input."""
        valid_play = False
        while(not valid_play):
            # input tile
            tile_notation = input(f" which tile does {self.color.upper()} place? ")

            # check for commands and run them
            if tile_notation != "" and tile_notation[0] == "\\":
                self.run_command(tile_notation[1:], game)
                continue

            # translate notation
            tile_coord = game.notation_to_coord(tile_notation)

            # avoid invalid tile notations
            if tile_coord == (-99, -99, -99):
                print(f"the tile '{tile_notation}' does not exist")
                continue

            illegal_move = game.place_tile(tile_coord, self.color)

            # report if move is illegal
            if illegal_move:
                print(f"move '{tile_notation}' is not allowed")
                continue
            else:
                valid_play = True
            
            # check for win
            win, _ = game.win_check(tile_coord, self.color)
            if win:
                print(f"{self.color} has won the game!")
            
            # check for captures
            capture_choice, _ = game.capture_check(tile_coord, self.color)
            if capture_choice:
                illegal_capture = True
                while illegal_capture:
                    notation_list = [game.coord_to_notation(coord) for coord in capture_choice]
                    capture = input(f"which tile does {self.color} capture from the following list {notation_list}? ")
                    capture = game.notation_to_coord(capture)
                    if capture in capture_choice:
                        illegal_capture =False
                        game.capture_tile(capture)
              
    def run_command(self, command: str, game: BokuGame):
        """this fuction is used to execute commands while the game loop is rnning"""
        command_dict = {
            "undo" : game.undo,
            "display" : game.draw_board,
            # i don't want to declare a wrapper function
            # this list comprehension converts from coordinates to notation
            "history" : lambda: print([[game.coord_to_notation(coord) for coord in action] for action in game.history]),
            "occupied": lambda: print(game.occupied_dict)
        }
        if command not in command_dict:
            print(f"command '\\{command}' is not a valid command")

        else:
            # run command
            data = command_dict[command]()

            # print command data
            print_list = []
            if command in print_list:
                print(data)
