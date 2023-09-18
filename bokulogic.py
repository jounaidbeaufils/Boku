import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon

class BokuGame:
  def __init__(self):
    self.all_coords = {(0, 0, 0), (-1, 1, 0), (-2, 2, 0), (-3, 3, 0), (-4, 4, 0), (-5, 5, 0), #A
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
    self.occupied_list = {}
    self.no_play_tile = tuple()
    self.history = []

    self.neibghbour_vectors = [(0,1,-1), #n
                        (0,-1,1), #s
                        (1,-1,0), #se
                        (-1,1,0), #nw
                        (-1,0,1), #sw
                        (1,0,-1)] #ne

    self.valid_notation = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 
                            'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 
                            'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 
                            'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 
                            'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10', 
                            'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 
                                  'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 
                                        'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 
                                              'I4', 'I5', 'I6', 'I7', 'I8', 'I9', 'I10', 
                                                    'J5', 'J6', 'J7', 'J8', 'J9', 'J10']

  def win_check(self, coord): #untested
    color = self.occupied_list[coord]
    for vect in self.neibghbour_vectors:
      curr_coord = coord
      for i in range(4): #we need to find 4 neighbours to make 5 in row
        xi, yi, zi = curr_coord
        new_coord = xi + vect[0], yi+ vect[1], zi + vect[2]

        if new_coord in self.occupied_list and self.occupied_list[new_coord] == color:
          curr_coord = new_coord
        else:
          break

        if i == 3:
          return True

    return False

  def capture_check(self, coord): #untested
    colors = []
    if self.occupied_list[coord] == "black":
      colors.extend(["white","white","black"])
    else:
      colors.extend(["black","black","white"])

    capture_choice = []
    for vect in self.neibghbour_vectors:
      xd, yd, zd = vect
      curr_coord = coord
      for i in range(3): #we need to find 4 neighbours to make a capture
        xi, yi, zi = curr_coord
        new_coord = xi + xd, yi + yd, zi + zd

        if new_coord in self.occupied_list and self.occupied_list[new_coord] == colors[i]:
          curr_coord = new_coord
        else:
          break
        if i == 2:
          x, y, z = coord
          capture_choice.extend([(x + xd, y + yd, z + zd), (x + xd*2, y + yd*2, z + zd*2)])

    return capture_choice

  def place_tile(self, coord, tile_color):
    win = False
    capture_choice = []
    illegal = False

    # check for if the tile is illegal
    if coord == self.no_play_tile or coord not in self.open_coord:
      illegal = True

    # perform legal move
    else:
      no_play_tile = tuple() #reset; tile is only blocked for one play

      # move tile from open to occupied and write history
      self.open_coord.remove(coord)
      self.occupied_list[coord] = tile_color
      self.history.append([coord])

      # check for win or captures
      win = self.win_check(coord)
      capture_choice = self.capture_check(coord)

    return win, capture_choice, illegal

  def capture_tile(self, tile, write_history=True):

    # move the tile from occupied to open and write history
    del self.occupied_list[tile]
    self.open_coord.add(tile) 
    if write_history:
      self.history[-1].append(tile) # added the removed tile on the last turn

    # block the tile for the next play
    self.no_play_tile = tile

  def draw_board(self):
    colors = [self.occupied_list.get(tuple(c), "blue") for c in self.all_coords]

    # Horizontal cartesian coords
    hcoord = [c[0] for c in self.all_coords]

    # Vertical cartesian coords
    vcoord = [2. * np.sin(np.radians(60)) * (c[1] - c[2]) / 3. for c in self.all_coords]

    fig, ax = plt.subplots(1, figsize=(10, 10))
    ax.set_aspect('equal')

    # Add some colored hexagons and labels
    for x, y, color, (xi, yi, zi) in zip(hcoord, vcoord, colors, self.all_coords):
      hexagon = RegularPolygon((x, y), numVertices=6, radius=2. / 3,
                                orientation=np.radians(30), facecolor=color,
                                alpha=0.3, edgecolor='k')
      ax.add_patch(hexagon)
      ax.text(x, y, BokuGame.coord_to_notation(xi,yi,zi), ha='center', va='center', fontsize=10)

    # Also add scatter points in hexagon centers ###remove?###
    ax.scatter(hcoord, vcoord, alpha=0.0)

    plt.show(block=False)

  def undo(self):
    """this function will undo the one players action"""
    action: str = self.history.pop()
    tile = ""
    capture = ""

    # checking if the last turn included a capture
    if len(action) > 1:
      tile, capture = action[0], action[1]
      self.place_tile(capture, False)

    else:
      tile = action[0]
    
    del self.occupied_list[tile]
    self.open_coord.add(tile)
      
  @staticmethod
  def notation_to_coord(notation):
    letter = notation[0].upper()
    z = -(ord(letter) - ord('A'))

    number = notation[1:]
    y = int(number) -1

    x = 1 - int(number) - z

    return x, y, z
  
  @staticmethod
  def coord_to_notation(x,y,z):
    notation = ""
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    notation += alpha[-z]
    notation += str(y + 1)

    return notation
  