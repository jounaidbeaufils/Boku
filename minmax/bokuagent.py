"""Module for all Boku agents."""
from random import randint, choice

from abc import ABC, abstractmethod
from bokuboard.bokulogic import BokuGame
from minmax.minmaxalgo import ab_negmax_random_capture

@abstractmethod
class BokuAgent(ABC):
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
    """Agent plays randomly."""
    def play(self, game: BokuGame):
        """Play a move."""
        # get all valid moves
        valid_moves = [move for move in game.occupied_dict if game.occupied_dict[move] == "free" and\
            move != game.no_play_tile]

        # check that their is a valid move
        if len(valid_moves) == 0:
            return False, None

        # choose a random move
        move_index = randint(0, len(valid_moves) - 1)
        move = valid_moves[move_index]

        # play the move
        game.place_tile(move, self.color)

        # combined heuristic, win and capture check
        win, capture_choice = game.heuristic_check(move, self.color, True)

        if capture_choice:
            capture = choice(list(capture_choice))
            game.capture_tile(capture)
            print(f"{self.color} RandomAgent captures {game.coord_to_notation(capture)}")

        return win, move


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

            # report if move is illegal and skip to next iteration
            if illegal_move:
                print(f"move '{tile_notation}' is not allowed")
                continue

            valid_play = True

            # check for captures
            win, capture_choice = game.heuristic_check(tile_coord, self.color, True)
            if capture_choice:
                illegal_capture = True
                while illegal_capture:
                    notation_list = [game.coord_to_notation(coord) for coord in capture_choice]
                    capture = input(f"which tile does {self.color.upper()} capture from the following list {notation_list}? ")
                    capture = game.notation_to_coord(capture)
                    if capture in capture_choice:
                        illegal_capture =False
                        game.capture_tile(capture)

        return win, tile_coord #TODO set up human skipping turn

class HeuristicAgent(BokuAgent):
    """Agent plays by using the first move in the priorityq."""

    def play(self, game: BokuGame):
        """Play a move. solely based on the best heuristic value"""
        #TODO remove illegal check, no longer needed, but implement turn skipping
        illegal = True
        while (illegal and len(game.heuristic["move order"]) > 0):
            move = game.heuristic["move order"].pop()
            move_coord = move.tile
            if move_coord == game.no_play_tile:
                if len(game.heuristic["move order"]) > 0: #another move is available
                    new_move = game.heuristic["move order"].pop()
                    game.heuristic["move order"].push(move)
                    move_coord = new_move.tile
                else:
                    break

            # play the move
            illegal = game.place_tile(move_coord, self.color)
            if illegal:
                print("the move is illegal")
                continue

            # combined heuristic, win and capture check
            win, capture_choice = game.heuristic_check(move_coord, self.color, True)

            if capture_choice:
                print(f"HeuristicAgent can capture one of the following tiles:{[BokuGame.coord_to_notation(coord) for coord in capture_choice]}")
                
                # capture at random because occupied tiles don't have a heuristic
                capture = choice(list(capture_choice))
                game.capture_tile(capture)
                print(f"{self.color} HeuristicAgent captures {game.coord_to_notation(capture)}")

        if illegal:
            print(f"{self.color} HeuristicAgent has no legal moves left")
            game.skip_turn()
            return False, None
        return win, move_coord

class ABNMAgentRandomCapture(BokuAgent):
    """Agent plays using a alpha-beta negamax search, will ask for ply depth at each turn.
       the agent will capture randomly when required to capture"""

    def __init__(self, color: str, depth:int=None):
        super().__init__(color)
        self.depth = depth
    
    def play(self, game: BokuGame):
        """play a move"""
        # check that a depth is given
        if self.depth is None:
            self.depth = int(input(f"what depth should the {self.color} agent search? "))

        # run search
        move, _ = ab_negmax_random_capture(node=game, depth=self.depth)

        # play the move
        game.place_tile(move, self.color)

        # combined heuristic, win and capture check
        win, capture_choice = game.heuristic_check(move, self.color, True)

        if win:
            return win, move

        # check if there is a capture
        if capture_choice:
            # play a random capture
            capture = choice(list(capture_choice))
            game.capture_tile(capture)
            print(f"{self.color} ABNMAgentRandomCapture captures {game.coord_to_notation(capture)}")

        return win, move
