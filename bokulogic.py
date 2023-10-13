"""this modul contains the BokuGame class"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon

import bokudata

class BokuGame: #TODO refactor the dictionarys into a seperate data class
    """the BokuGame class contains all the functions required to play the BokuGame.
       Also includes a function to display the board using matplotlib"""
    def __init__(self):
        self.all_coords = {
            (0, 0, 0), (-1, 1, 0), (-2, 2, 0), (-3, 3, 0), (-4, 4, 0), (-5, 5, 0), #A
            (1, 0, -1), (0, 1, -1), (-1, 2, -1), (-2, 3, -1), (-3, 4, -1), (-4, 5, -1), (-5, 6, -1), #B
            (2, 0, -2), (1, 1, -2), (0, 2, -2), (-1, 3, -2), (-2, 4, -2), (-3, 5, -2), (-4, 6, -2), (-5, 7, -2), #C
            (3, 0, -3), (2, 1, -3), (1, 2, -3), (0, 3, -3), (-1, 4, -3), (-2, 5, -3), (-3, 6, -3), (-4, 7, -3), (-5, 8, -3), #D
            (4, 0, -4), (3, 1, -4), (2, 2, -4), (1, 3, -4), (0, 4, -4), (-1, 5, -4), (-2, 6, -4), (-3, 7, -4), (-4, 8, -4), (-5, 9, -4), #E
            (5, 0, -5), (4, 1, -5), (3, 2, -5), (2, 3, -5), (1, 4, -5), (0, 5, -5), (-1, 6, -5), (-2, 7, -5), (-3, 8, -5), (-4, 9, -5), #F
            (5, 1, -6), (4, 2, -6), (3, 3, -6), (2, 4, -6), (1, 5, -6), (0, 6, -6), (-1, 7, -6), (-2, 8, -6), (-3, 9, -6), #G
            (5, 2, -7), (4, 3, -7), (3, 4, -7), (2, 5, -7), (1, 6, -7), (0, 7, -7), (-1, 8, -7), (-2, 9, -7), #H
            (5, 3, -8), (4, 4, -8), (3, 5, -8), (2, 6, -8), (1, 7, -8), (0, 8, -8), (-1, 9, -8), #I
            (5, 4, -9), (4, 5, -9), (3, 6, -9), (2, 7, -9), (1, 8, -9), (0, 9, -9)} #J

        self.open_coord = self.all_coords.copy()
        self.occupied_dict = {coord : "free" for coord in bokudata.all_coords}
        self.no_play_tile = tuple()
        self.history = []

        self.neibghbour_vectors = [(0,1,-1), #n
                                   (1,0,-1), #ne
                                   (-1,1,0), #nw
                                   (0,-1,1), #s
                                   (1,-1,0), #se
                                   (-1,0,1)] #sw

        self.valid_notation =  {'A1', 'A2', 'A3', 'A4', 'A5', 'A6',
                                'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 
                                'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 
                                'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 
                                'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10', 
                                'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 
                                      'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 
                                            'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 
                                                  'I4', 'I5', 'I6', 'I7', 'I8', 'I9', 'I10', 
                                                        'J5', 'J6', 'J7', 'J8', 'J9', 'J10'}
        
        self.centricity_values = {
            (-3, 4, -1): 22, (2, 1, -3): 22, (2, 2, -4): 25, (-2, 8, -6): 22, (-4, 5, -1): 21, (-2, 9, -7): 19, (-3, 8, -5): 22,
            (0, 2, -2): 24, (1, 0, -1): 19, (-2, 6, -4): 27, (-2, 7, -5): 25, (1, 5, -6): 28, (1, 6, -7): 25, (-4, 9, -5): 19,
            (4, 2, -6): 21, (-3, 6, -3): 24, (-3, 7, -4): 24, (2, 6, -8): 22, (2, 7, -9): 19, (0, 9, -9): 18, (1, 3, -4): 28,
            (1, 4, -5): 30, (-4, 7, -3): 21, (-3, 5, -2): 24, (4, 1, -5): 21, (-1, 2, -1): 22, (-5, 7, -2): 18, (0, 0, 0): 18,
            (5, 4, -9): 18, (0, 7, -7): 24, (-1, 6, -5): 28, (4, 0, -4): 19, (-5, 5, 0): 18, (5, 2, -7): 18, (-5, 6, -1): 18,
            (-1, 5, -4): 30, (5, 1, -6): 18, (0, 4, -4): 30, (0, 5, -5): 30, (1, 7, -8): 22, (4, 4, -8): 21, (-2, 3, -1): 22,
            (-1, 3, -2): 25, (-1, 4, -3): 28, (-3, 9, -6): 19, (4, 5, -9): 19, (5, 0, -5): 18, (0, 3, -3): 27, (3, 1, -4): 22,
            (3, 2, -5): 24, (4, 3, -7): 21, (-5, 9, -4): 18, (3, 0, -3): 19, (2, 0, -2): 19, (-4, 8, -4): 21, (-1, 1, 0): 19,
            (-5, 8, -3): 18, (-1, 8, -7): 22, (-1, 9, -8): 19, (0, 8, -8): 21, (3, 6, -9): 19, (-4, 6, -2): 21, (-2, 5, -3): 27,
            (-1, 7, -6): 25, (5, 3, -8): 18, (0, 6, -6): 27, (3, 5, -8): 22, (0, 1, -1): 21, (2, 5, -7): 25, (-2, 4, -2): 25,
            (1, 2, -3): 25, (3, 3, -6): 24, (-3, 3, 0): 19, (3, 4, -7): 24, (2, 3, -5): 27, (1, 8, -9): 19, (2, 4, -6): 27,
            (-2, 2, 0): 19, (1, 1, -2): 22, (-4, 4, 0): 19}
        
        self.heuristic = {
            "win" : {coord : 0 for coord in bokudata.all_coords},
            "capture" : {coord : 0 for coord in bokudata.all_coords},
            "centricity" : bokudata.centricity_values}
        
    def win_check(self, coord: tuple, win_color: str): # TODO access the common heuristic directly, and clean it before overwriting
        """this function checks for a win and also returns the value of every tile on the axi,
        this value is the contribution that this tile, if placed, contributes to a win on """

        opp_color = "white" if win_color == "black" else "black"

        value_dict = {}
        win = False
        # get the three axi
        for vect in self.neibghbour_vectors[0:3]:
            line_coords = []
            # get the positions in each axis
            for i in range(-4,5):
                line_coord = (coord[0] + vect[0]*i, coord[1] + vect[1]*i, coord[2] + vect[2]*i)
                if line_coord in self.occupied_dict:
                    line_coords.append(line_coord)
                    value_dict[line_coord] = 0

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
                    return win, value_dict

                if sum(sub_line_addition) > 0:
                    for t_n, value in enumerate(sub_line_addition):
                        value_dict[line_coords[s_l + t_n]] += value / counter

        for d_coord, d_value in value_dict.items():
            self.heuristic["win"][d_coord] = d_value #TODO: override or add?

        return win, value_dict

    def capture_check(self, coord: tuple, capture_color: str, recursive: bool=True): # TODO access the common heuristic directly, and clean it before overwriting
        """this function checks for a win and also returns the value of every tile on the axi,
        this value is the contribution that this tile, if placed, contributes to a win on """

        capture_pattern = []
        if capture_color == "white":
            capture_pattern = ["white", "black", "black", "white"]
        else:
            capture_pattern = ["black", "white", "white", "black"]

        value_dict = {}
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

                # check if a capture hasoccured
                if pattern_match_count == 4:
                    # add the second and third tiles as capturable
                    capture_choice.add(line_coords[s_l + 1])
                    capture_choice.add(line_coords[s_l + 2])

                # run a capture check for the other color, to update the heuristic
                # ignore the capture as it it not the opponents turn
                if recursive:
                    opp_color = "white" if capture_color == "black" else "black"
                    self.capture_check(line_coords[s_l + 3], opp_color, recursive=False)

        for d_coord, d_value in value_dict.items():
            self.heuristic["capture"][d_coord] = d_value #TODO: override or add?

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
            self.open_coord.remove(coord)
            self.occupied_dict[coord] = tile_color
            if write_history:
                self.history.append([coord])

        return illegal

    def capture_tile(self, tile, write_history=True):
        """captes the tile it recieved in paramaters and locks that tile"""

        # move the tile from occupied to open and write history
        self.occupied_dict[tile] = "free"
        self.open_coord.add(tile)
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

    def draw_board(self):
        """draw the board"""

        colors = [self.occupied_dict.get(tuple(c), "blue") for c in self.all_coords]
        colors = [color if color != "free" else "blue" for color in colors]

        # Horizontal cartesian coords
        hcoord = [c[0] for c in self.all_coords]

        # Vertical cartesian coords
        vcoord = [2. * np.sin(np.radians(60)) * (c[1] - c[2]) / 3. for c in self.all_coords]

        _, ax = plt.subplots(1, figsize=(10, 10))
        ax.set_aspect('equal')

        # Add some colored hexagons and labels
        for x, y, color, coord in zip(hcoord, vcoord, colors, self.all_coords):
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
        if notation.upper() in self.valid_notation:
            letter = notation[0].upper()
            coord[2] = -(ord(letter) - ord('A'))

            number = notation[1:]
            coord[1] = int(number) -1

            coord[0] = 1 - int(number) - coord[2]

        return tuple(coord)

    def coord_to_notation(self, coord):
        """will return an empty string if the coord is not on the boord"""

        notation = ""
        if coord in self.all_coords:
            notation = ""
            alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

            notation += alpha[-coord[2]]
            notation += str(coord[1] + 1)

        return notation
  