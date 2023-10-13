"""Module for all Boku agents."""
from random import randint, choice

from abc import ABC, abstractmethod
from bokulogic import BokuGame

@abstractmethod
class BokuAgent(ABC): # TODO update agents to use heuristics properly
    """Abstract base class for all Boku agents."""
    def __init__(self, color: str):
        self.color = color

    @abstractmethod
    def play(self, game: BokuGame) -> tuple():
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
        move = valid_moves[move_index]

        # play the move
        game.place_tile(move, self.color)
        print(f"{self.color} RandomAgent plays {game.coord_to_notation(move)}")

        # capture if possible
        capture_choice, _ = game.capture_check(move, self.color)
        if capture_choice:
            capture = choice(list(capture_choice))
            game.capture_tile(capture)
            print(f"{self.color} RandomAgent captures {game.coord_to_notation(capture)}")

        return move


class HumanAgent(BokuAgent):
    """Class for human players."""
    def play(self, game: BokuGame):
        """Play a move by asking the user for input."""
        valid_play = False
        tile_coord = tuple()
        while(not valid_play):
            # input tile
            tile_notation = input(f"which tile does {self.color.upper()} place? ")

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

            # check for captures
            capture_choice, _ = game.capture_check(tile_coord, self.color)
            if capture_choice:
                illegal_capture = True
                while illegal_capture:
                    notation_list = [game.coord_to_notation(coord) for coord in capture_choice]
                    capture = input(f"which tile does {self.color.upper()} capture from the following list {notation_list}? ")
                    capture = game.notation_to_coord(capture)
                    if capture in capture_choice:
                        illegal_capture =False
                        game.capture_tile(capture)

        return tile_coord
