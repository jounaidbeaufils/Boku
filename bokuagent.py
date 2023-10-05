"""Module for all Boku agents."""
from abc import ABC, abstractmethod
from bokulogic import BokuGame

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
