"""this modul contains the BokuGame class"""
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon

from bokuboard import bokudata
from bokuboard.sumtrackingdict import SumTrackingDictWithUndo
from priorityq.mapped_queue import MappedQueueWithUndo
from minmax.heuristictile import HeuristicTile

from privatedebug.utils import warn_if_called_outside_class, restrict_to_class

class BokuGame:
    """the BokuGame class contains all the functions required to play the BokuGame.
       Also includes a function to display the board using matplotlib"""
    def __init__(self):
        self.occupied_dict = {coord : "free" for coord in bokudata.all_coords}
        self.no_play_tile = tuple()

        self.history = []
        self.heuristic_undo_tracker = []

        self.neibghbour_vectors = [(0,1,-1), #n
                                   (1,0,-1), #ne
                                   (-1,1,0), #nw
                                   (0,-1,1), #s
                                   (1,-1,0), #se
                                   (-1,0,1)] #sw

        self.heuristic = {
            "move order" : MappedQueueWithUndo(),
            "centricity" : bokudata.centricity_values_normalized,
            "white" : SumTrackingDictWithUndo(),
            "black" : SumTrackingDictWithUndo(),
            "winner": ""}

        for coord, value in bokudata.centricity_values.items():
            self.heuristic["move order"].push(HeuristicTile(coord, value * -1))

    @restrict_to_class
    def _win_check(self, coord: tuple, win_color: str):
        """this function checks for a win and also returns the value of every tile on the axi,
        this value is the contribution that this tile, if placed, contributes to a win on """

        opp_color = "white" if win_color == "black" else "black"

        value_dict = defaultdict(int)
        win = False
        # get the three axi
        for vect in self.neibghbour_vectors[0:3]:
            line_coords = []
            # get the positions in each axis
            for i in range(-4,5):
                line_coord = (coord[0] + vect[0]*i, coord[1] + vect[1]*i, coord[2] + vect[2]*i)
                if line_coord in self.occupied_dict:
                    line_coords.append(line_coord)

            # for every sub_line in a line
            for s_l in range(len(line_coords) - 4):
                counter = 0
                sub_line_addition = [0 for _ in range(5)]

                # every tile n in a sub_line
                for t_n in range(5):
                    if self.occupied_dict[line_coords[s_l + t_n]] == opp_color:
                        sub_line_addition[t_n] = -99
                        break
                    if self.occupied_dict[line_coords[s_l + t_n]]  == "free":
                        sub_line_addition[t_n] = 1
                        counter += 1

                if sum(sub_line_addition) == 0:
                    win = True
                    return win, {}

                if sum(sub_line_addition) > 0:
                    for t_n, value in enumerate(sub_line_addition):
                        value_dict[line_coords[s_l + t_n]] += value / counter

        return win, value_dict

    @restrict_to_class
    def _capture_check(self, coord: tuple, capture_color: str):
        """this function checks for a win and also returns the value of every tile on the axi,
        this value is the contribution that this tile, if placed, contributes to a win on """

        capture_pattern = []
        if capture_color == "white":
            capture_pattern = ["white", "black", "black", "white"]
        else:
            capture_pattern = ["black", "white", "white", "black"]

        value_dict = defaultdict()
        capture_choice = set()

        # get the three axi
        for vect in self.neibghbour_vectors:
            line_coords = []
            # get the positions in each axis
            for i in range(-3,4):
                line_coord = (coord[0] + vect[0]*i, coord[1] + vect[1]*i, coord[2] + vect[2]*i)

                # check that the tile is on the board
                if line_coord in self.occupied_dict:
                    # add the coordinate
                    line_coords.append(line_coord)
                    #value_dict[line_coord] = 0

            # for every sub_line in a line
            for s_l in range(len(line_coords) - 3):
                pattern_match_count = 0

                # every tile n in a sub_line
                for i, t_n in enumerate(range(4)):

                    # break if the tile does not match the pattern
                    if self.occupied_dict[line_coords[s_l + t_n]] == capture_pattern[i]:
                        pattern_match_count += 1
                    else:
                        break

                # check if a capture is available next turn
                if pattern_match_count == 3:
                    value_dict[line_coords[s_l + 3]] = 1

                # check if a capture has occured
                if pattern_match_count == 4:
                    # add the second and third tiles as capturable
                    capture_choice.add(line_coords[s_l + 1])
                    capture_choice.add(line_coords[s_l + 2])

        return capture_choice, value_dict

    @warn_if_called_outside_class
    def _place_tile(self, coord, tile_color, write_history=True) -> bool:
        """places a tile, and then calls win check and capture check"""

        # check for if the tile is illegal
        illegal = False
        if coord == self.no_play_tile or self.occupied_dict[coord] != "free":
            illegal = True

        # perform legal move
        else:
            # reset no_play_tile; tile is only blocked for one play
            self.no_play_tile = tuple()

            # move tile from open to occupied and write history
            self.occupied_dict[coord] = tile_color
            if write_history:
                # write the move to history
                self.history.append([coord])

                # add the heuristic undo tracker entry
                # for every boiard undo multiple undos are required on the heuristic data structures
                self.heuristic_undo_tracker.append([0,0,0])

                # remove a tile that is placed from the move order heuristic
                # it is no longer a move that should be played
                self.heuristic["move order"].remove(HeuristicTile(coord, 0))

                # add to the heuristic undo tracker
                self.heuristic_undo_tracker[-1][0] += 1

        return illegal

    def skip_turn(self):
        """skips the turn of the player who's turn it is"""
        # consider adding two skip turns to the move order heuristic

        # write history as empty turn
        self.history.append([""])

        # ensuring that when a move is undone the right number of heuristic changes have been undone
        self.heuristic_undo_tracker.append([0,0,0])

        #reset no_play_tile. it is only blocked for one play
        self.no_play_tile = tuple()

    @warn_if_called_outside_class
    def _capture_tile(self, tile, write_history=True):
        """captes the tile it recieved in paramaters and locks that tile"""
        #TODO consider making capture_check run heuristics.
        # however heuristics are currently called by Agents
        # wrapper functions for play_tile and play_capture should be made

        # move the tile from occupied to open
        self.occupied_dict[tile] = "free"

        # write move to history
        if write_history:

            # add the removed tile on the latest turn's entry
            self.history[-1].append(tile)

            # return the tile to the move order heuristic
            heuristic_tile = HeuristicTile(tile, bokudata.centricity_values_normalized[tile] * -1)
            self.heuristic["move order"].push(heuristic_tile)

            # add to the heuristic undo tracker
            self.heuristic_undo_tracker[-1][0] += 1

    @warn_if_called_outside_class
    def _win_capture_check(self, coord, color, can_capture) -> tuple():
        """runs all required heuristics that should be played when a move is played
        a move includes a tile placement and a capture, 
        the move is passed as the coord of the tile placed or captured.

        for efficiency, heuristic_check will also be used to check for wins and captures
        """
        #TODO can_capture is no longer used, remove.

        # set opposition color
        opp_color = "white" if color == "black" else "black"

        # check for win by the player who just moved
        color_win, color_win_dict = self._win_check(coord, color)

        # early exit out of heuristic when a game is won
        if can_capture and color_win:
            self.heuristic["winner"] = color
            return color_win, set()

        # check for win by the opposite player
        #TODO improve heuristic accuracy with update order and potentially recursion
        _, opp_win_dict = self._win_check(coord, opp_color)

        # check for captures after a capture, to update the heuristic
        color_choice, color_capture_dict = self._capture_check(coord, color)
        _, opp_capture_dict = self._capture_check(coord, opp_color)

        # update the heuristics
        self._heuristic_update(color_capture_dict, color_win_dict, color)
        self._heuristic_update(opp_capture_dict, opp_win_dict, opp_color)

        # return the win state (false) and capture choices
        if can_capture:
            return False, color_choice

        else:
            return False, set()

    @restrict_to_class
    def _heuristic_update(self, capture_value_dict, win_value_dict, color, weights=None):
        """push heuristic values to the heuristic dicts"""

        # set default weights
        if weights is None:
            weights = {"capture": 1, "win": 1, "centricity": 1}

        # combine capture and win value dicts
        combined_value_dict = capture_value_dict.copy()

        for key, value in win_value_dict.items():
            if key not in combined_value_dict:
                # set the value to 0 if it is not in the dict
                combined_value_dict[key] = 0
            else:
                # scale the value by the capture weight
                combined_value_dict[key] *= weights["capture"]

            # add the weighted win value to the capture value
            combined_value_dict[key] += value * weights["win"]

            # add the centricity value to the capture value
            combined_value_dict[key] += self.heuristic["centricity"][key] * weights["centricity"]

            # flip heuristic sign, because the priorityq is a min queue
            combined_value_dict[key] *= -1

        # update the heuristics
        move_order_changes = 0
        color_changes = 0
        for key, value in combined_value_dict.items():
            if self.occupied_dict[key] == "free":
                # update the player whos turn it is
                self.heuristic[color][key] = value
                color_changes += 1

                # update the move ordering peiority queue
                self.heuristic["move order"].update(HeuristicTile(key, 0),
                                                    HeuristicTile(key, value))
                move_order_changes += 1

        # add the heuristic change to the heuristic undo tracker
        # the heuristic data structures can undo past changes
        # but the are changed multiple times a turn
        self.heuristic_undo_tracker[-1][0] += move_order_changes

        # white and black have their own heuristic per turn
        color_pos = 1 if color == "white" else 2
        self.heuristic_undo_tracker[-1][color_pos] += color_changes

    def play_tile(self, coord, color):
        """play a tile, and then call win check and capture check
            intended as a one move call for agents
            making play_capture the only other call
        """
        illegal = True
        win = False
        capture_choice = set()

        # attempt to play the tile
        illegal = self._place_tile(coord, color)

        if not illegal:
            # check for win and capture, if the tile was placed
            win, capture_choice = self._win_capture_check(coord, color, True)

        return illegal, win, capture_choice

    def play_capture(self, capture, capture_choice):
        """play a capture, and then call win check and capture check
            intended as a one move call for agents
            making play_tile the only other call
        """

        illegal = True
        # check if the capture is legal
        if capture in capture_choice:
            illegal = False
            color = "white" if len(self.history) % 2 == 0 else "black"

            # perform legal capture
            self._capture_tile(capture, True)

            # update the heuristics
            #TODO this line is causing errors in the undo process
            #_, _ = self._win_capture_check(capture, color, False)

        return illegal

    def draw_board(self):
        """draw the board"""

        colors = [self.occupied_dict.get(tuple(c), "blue") for c in bokudata.all_coords]
        colors = [color if color != "free" else "blue" for color in colors]

        # Horizontal cartesian coords
        hcoord = [c[0] for c in bokudata.all_coords]

        # Vertical cartesian coords
        vcoord = [2. * np.sin(np.radians(60)) * (c[1] - c[2]) / 3. for c in bokudata.all_coords]

        _, ax = plt.subplots(1, figsize=(10, 10))
        ax.set_aspect('equal')

        # Add some colored hexagons and labels
        for x, y, color, coord in zip(hcoord, vcoord, colors, bokudata.all_coords):
            hexagon = RegularPolygon((x, y), numVertices=6, radius=2. / 3,
                                      orientation=np.radians(30), facecolor=color,
                                      alpha=0.3, edgecolor='k')
            ax.add_patch(hexagon)
            ax.text(x, y, bokudata.coord_to_notation(coord), ha='center', va='center', fontsize=10)

        # Also add scatter points in hexagon centers ###remove?###
        ax.scatter(hcoord, vcoord, alpha=0.0)

        plt.show(block=False)

    def undo(self):
        """this function will undo the one players action"""

        if self.history:
            ## undo the changes to the board
            captured_color = "white" if len(self.history) % 2 == 0 else "black"
            action = self.history.pop()

            # conditonal for the edge case when undoning the first move
            previous_action = self.history[-1] if self.history else [tuple(), tuple()]
            tile = ""
            captured = ""

            # checking if the last turn included a capture
            if len(action) > 1:
                # set the placed tile and the captured tile
                tile, captured = action[0], action[1]

                #reset the no_play_tile because the capture was undone
                self.no_play_tile = tuple()

                # replace the captured tile without writing to history
                self._place_tile(captured,captured_color,False)

            else:
                # set the placed tile
                tile = action[0]

            # after the undo if we are right after a capture, so set the no_play_tile
            if len(previous_action) > 1:
                self.no_play_tile = previous_action[1]

            # if the tile is not empty, then a tile was placed (for skipped turns)
            if tile != "":
                # remove the tile played using capture without writing to history
                # write_history=False also disables the tile lock
                self._capture_tile(tile, False)


            ## undo the changes to the heuristics

            move_order, white, black = self.heuristic_undo_tracker.pop()
            #print(f"move order: {move_order}, white: {white}, black: {black}")
            # move order heuristic undo
            for _ in range(move_order):
                self.heuristic["move order"].undo()

            # white heuristic undo
            for _ in range(white):
                self.heuristic["white"].undo()

            # black heuristic undo
            for _ in range(black):
                self.heuristic["black"].undo()

            # reset the winner
            self.heuristic["winner"] = ""

        return action #TODO what is this for?

    def eval(self):
        """evaluate the game state and return a value"""
        #TODO this function should be replaced by different functions for different agents
        # return a value if not win
        if self.heuristic["winner"] == "":
            return round((self.heuristic["black"].total() - self.heuristic["white"].total()) * 1000)

        # return a value for white win
        if self.heuristic["winner"] == "white":
            return 100000

        # return a value for white loss
        if self.heuristic["winner"] == "black":
            return -100000

        # return a value for draw
        else:
            return 90000
