"""this modul contains the BokuGame class"""
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon

from bokuboard import bokudata
from bokuboard.sumtrackingdict import SumTrackingDict
from priorityq.mapped_queue import MappedQueueWithUndo
from minmax.heuristictile import HeuristicTile

class BokuGame:
    """the BokuGame class contains all the functions required to play the BokuGame.
       Also includes a function to display the board using matplotlib"""
    def __init__(self):
        self.occupied_dict = {coord : "free" for coord in bokudata.all_coords}
        self.no_play_tile = tuple()
        self.history = []

        self.neibghbour_vectors = [(0,1,-1), #n
                                   (1,0,-1), #ne
                                   (-1,1,0), #nw
                                   (0,-1,1), #s
                                   (1,-1,0), #se
                                   (-1,0,1)] #sw
        
        self.heuristic = {
            "move order" : MappedQueueWithUndo(),
            "centricity" : bokudata.centricity_values_normalized,
            "white" : SumTrackingDict(),
            "black" : SumTrackingDict()}
        
    def win_check(self, coord: tuple, win_color: str):
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

    def capture_check(self, coord: tuple, capture_color: str):
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

    def place_tile(self, coord, tile_color, write_history=True):
        """places a tile, and then calls win check and capture check"""

        illegal = False

        # check for if the tile is illegal
        if coord == self.no_play_tile or self.occupied_dict[coord] != "free":
            illegal = True

        # perform legal move
        else:
            self.no_play_tile = tuple() #reset; tile is only blocked for one play

            # move tile from open to occupied and write history
            self.occupied_dict[coord] = tile_color
            if write_history:
                self.history.append([coord])

        return illegal

    def capture_tile(self, tile, write_history=True):
        """captes the tile it recieved in paramaters and locks that tile"""

        # move the tile from occupied to open and write history
        self.occupied_dict[tile] = "free"
        if write_history:
            # add the removed tile on the last turn's entry
            self.history[-1].append(tile)

            # block the tile for the next play
            self.no_play_tile = tile

            # check for captures after a capture, to update the heuristic
            self.capture_check(tile, "white")
            self.capture_check(tile, "black")

            # check for wins after a capture, to update the heuristic
            self.win_check(tile, "white")
            self.win_check(tile, "black")

    def heuristic_check(self, coord, color, can_capture) -> tuple():
        """runs all required heuristics that should be played when a move is played
        a move includes a tile placement and a capture, 
        the move is passed as the coord of the tile placed or captured.

        for efficiency, heuristic_check will also be used to check for wins and captures
        """
        # set opposition color
        opp_color = "white" if color == "black" else "black"

        # check for win by the player who just moved
        color_win, color_win_dict = self.win_check(coord, color)

        # early exit out of heuristic when a game is won
        if can_capture and color_win:
            return color_win, set()

        # check for win by the oppositit player
        #TODO improve heuristic accuracy with update order and potentially recursion
        _, opp_win_dict = self.win_check(coord, opp_color)

        # check for captures after a capture, to update the heuristic
        color_choice, color_capture_dict = self.capture_check(coord, color)
        _, opp_capture_dict = self.capture_check(coord, opp_color)

        # update the heuristics
        self.heuristic_update(color_capture_dict, color_win_dict, color)
        self.heuristic_update(opp_capture_dict, opp_win_dict, opp_color) # str on pupose as it will cause an error if the value is read

        # return the win state (false) and capture choices
        if can_capture:
            return False, color_choice
        
        else:
            return False, set()

    def heuristic_update(self, capture_value_dict, win_value_dict, color, weights=None):
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

        # update the heuristics
        for key, value in combined_value_dict.items():
            # update the player whos turn it is
            self.heuristic[color][key] = value

            # update the move ordering peiority queue
            self.heuristic["move order"].push(HeuristicTile(key, value))



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
            ax.text(x, y, self.coord_to_notation(coord), ha='center', va='center', fontsize=10)

        # Also add scatter points in hexagon centers ###remove?###
        ax.scatter(hcoord, vcoord, alpha=0.0)

        plt.show(block=False)

    def undo(self):
        """this function will undo the one players action"""

        if self.history:
            captured_color = "white" if len(self.history) % 2 == 0 else "black"
            action = self.history.pop()
            previous_action = self.history[-1]
            tile = ""
            captured = ""

            # checking if the last turn included a capture
            if len(action) > 1:
                tile, captured = action[0], action[1]

                #reset the no_play_tile because the capture was undone
                self.no_play_tile = tuple()

                # replace the captured tile without writing to history
                self.place_tile(captured,captured_color,False)

            # after the undo if we are right after a capture, set the no_play_tile
            if len(previous_action) > 1:
                self.no_play_tile = previous_action[1]

            else:
                tile = action[0]

            # remove the tile played using capture without writing to history
            # wriet_history=False also disables the tile lock
            self.capture_tile(tile, False)

        return action

    def notation_to_coord(self, notation: str):
        """will return (-99, -99, -99) if the notation is invalid"""

        coord = [-99, -99, -99]
        if notation.upper() in bokudata.valid_notation:
            letter = notation[0].upper()
            coord[2] = -(ord(letter) - ord('A'))

            number = notation[1:]
            coord[1] = int(number) -1

            coord[0] = 1 - int(number) - coord[2]

        return tuple(coord)

    def coord_to_notation(self, coord):
        """will return an empty string if the coord is not on the boord"""

        notation = ""
        if coord in bokudata.all_coords:
            notation = ""
            alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

            notation += alpha[-coord[2]]
            notation += str(coord[1] + 1)

        return notation
  