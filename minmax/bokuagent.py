"""Module for all Boku agents."""
from random import randint, choice

from abc import ABC, abstractmethod
from bokuboard.bokulogic import BokuGame
from bokuboard.bokudata import coord_to_notation, notation_to_coord
from minmax.minmaxalgo import ab_negmax_capture_tt, ab_negmax_capture_tt_2, ab_negmax_random_capture, ab_negmax_with_capture, ab_negmax_with_capture_2
from minmax.transitiontable import LRUCacheWithDefault
from userinputs.commands import run_command

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
        valid_moves = [move for move in game.occupied_dict if game.occupied_dict[move] == "free"
            and move != game.no_play_tile]

        # check that their is a valid move
        if len(valid_moves) == 0:
            return False, None

        # choose a random move
        move_index = randint(0, len(valid_moves) - 1)
        move = valid_moves[move_index]

        # play the move
        _, win, capture_choice = game.play_tile(move, self.color)

        # check if there is a capture
        if capture_choice:
            # play a random capture
            capture = choice(list(capture_choice))
            game.play_capture(capture, capture_choice)

        return win, move

class HumanAgent(BokuAgent):
    """Class for human players."""
    def play(self, game: BokuGame):
        """Play a move by asking the user for input."""
        valid_play = False
        tile_coord = tuple()
        while not valid_play:
            # input tile
            tile_notation = input(f"which tile does {self.color.upper()} place? ")

            # check for commands
            if tile_notation[0] == "\\":
                run_command(tile_notation[1:], game)
                continue

            if tile_notation == "skip":
                game.skip_turn()
                return False, "skip"

            # translate notation
            tile_coord = notation_to_coord(tile_notation)

            # avoid invalid tile notations
            if tile_coord == (-99, -99, -99):
                print(f"the tile '{tile_notation}' does not exist")
                continue

            # play the tile
            illegal, win, capture_choice = game.play_tile(tile_coord, self.color)

            # report if move is illegal and skip to next iteration
            if illegal:
                print(f"move '{tile_notation}' is not allowed")
                continue

            valid_play = True

            if capture_choice:
                illegal_capture = True
                while illegal_capture:
                    notation_list = [coord_to_notation(coord) for coord in capture_choice]
                    capture = input(
                        f"which tile does {self.color.upper()} capture from {notation_list}? ")
                    capture = notation_to_coord(capture)
                    illegal_capture = game.play_capture(capture, capture_choice)

        return win, tile_coord

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
                # if another move is available
                #!TODO this will mess with the undo. but the agent is not used
                if len(game.heuristic["move order"]) > 0:
                    new_move = game.heuristic["move order"].pop()
                    game.heuristic["move order"].push(move)
                    move_coord = new_move.tile
                else:
                    break

            # play the move
            illegal, win, capture_choice = game.play_tile(move_coord, self.color)
            if illegal:
                print("the move is illegal")
                continue

            if capture_choice:
                # capture at random because occupied tiles don't have a heuristic
                capture = choice(list(capture_choice))
                game.play_capture(capture, capture_choice)

        # TODO implement turn skipping, properly
        if illegal:
            game.skip_turn()
            return False, "skip"
        return win, move_coord

class ABNMBokuAgent(BokuAgent):
    """Agent plays using a alpha-beta negamax search."""

class ABNMAgentRandomCapture(ABNMBokuAgent):
    """Agent plays using a alpha-beta negamax search,
       the agent will capture randomly when required to capture"""

    def __init__(self, color: str, depth:int):
        super().__init__(color)
        self.depth = depth

    def play(self, game: BokuGame):
        """play a move"""

        # run search
        move, _ = ab_negmax_random_capture(node=game, depth=self.depth)

        if move is None:
            game.skip_turn()
            return False, "skip"

        # play the move
        _, win, capture_choice = game.play_tile(move, self.color)

        if win:
            return win, move

        # check if there is a capture
        if capture_choice:
            # play a random capture
            capture = choice(list(capture_choice))
            game.play_capture(capture, capture_choice)
        return win, move

class ABNMAgentWithCapture(ABNMBokuAgent):
    """Agent plays using a alpha-beta negamax search,
       the agent will capture randomly when required to capture"""

    def __init__(self, color: str, depth:int):
        super().__init__(color)
        self.depth = depth

    def play(self, game: BokuGame):
        """play a move"""

        # run search
        move, capture, _ = ab_negmax_with_capture_2(node=game, depth=self.depth)

        if move is None:
            game.skip_turn()
            return False, "skip"

        # play the move
        _, win, capture_choice = game.play_tile(move, self.color)
        if capture_choice:
            print("was a capture played when required to capture?")
        if win:
            return win, move

        # check if there is a capture
        if capture is not None:
            # play capture
            game.play_capture(capture, capture_choice)
        return win, move

class ABNMAgentWithTT(ABNMBokuAgent):
    """Agent plays using a alpha-beta negamax search with a transposition table."""
    def __init__(self, color: str, depth:int):
        super().__init__(color)
        self.depth = depth
        self.tt = LRUCacheWithDefault(100000, lambda: {'depth': -1})

    def play(self, game: BokuGame):
        """play a move"""

        # run search
        move, capture, _ = ab_negmax_capture_tt_2(node=game, depth=self.depth)


        if move is None:
            game.skip_turn()
            return False, "skip"

        # play the move
        _, win, capture_choice = game.play_tile(move, self.color)

        if win:
            return win, move

        # check if there is a capture
        if capture is not None:
            # play capture
            game.play_capture(capture, capture_choice)
        return win, move
