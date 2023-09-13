class BokuGame:
  def __init__(self):
    self.open_coord = set([(0,0,0), (-1,1,0), (-2,2,0), (-3,3,0), (-4,4,0), (-5,5,0), #A
                (1,0,-1), (0,1,-1), (-1,2,-1), (-2,3-1), (-3,4,-1), (-4,5,-1), (-5,6,-1), #B
                (2, 0, -2), (1, 1, -2), (0, 2, -2), (-1, 3, -2), (-2, 4, -2), (-3, 5, -2), (-4, 6, -2), (-5, 7, -2), #C
                (3, 0, -3), (2, 1, -3), (1, 2, -3), (0, 3, -3), (-1, 4, -3), (-2, 5, -3), (-3, 6, -3), (-4, 7, -3), (-5, 8, -3), #D
                (4, 0, -4), (3, 1, -4), (2, 2, -4), (1, 3, -4), (0, 4, -4), (-1, 5, -4), (-2, 6, -4), (-3, 7, -4), (-4, 8, -4), (-5, 9, -4), #E
                (5, 0, -5), (4, 1, -5), (3, 2, -5), (2, 3, -5), (1, 4, -5), (0, 5, -5), (-1, 6, -5), (-2, 7, -5), (-3, 8, -5), (-4, 9, -5), #F
                (5, 1, -6), (4, 2, -6), (3, 3, -6), (2, 4, -6), (1, 5, -6), (0, 6, -6), (-1, 7, -6), (-2, 8, -6), (-3, 9, -6), #G
                (5, 2, -7), (4, 3, -7), (3, 4, -7), (2, 5, -7), (1, 6, -7), (0, 7, -7), (-1, 8, -7), (-2, 9, -7), #H
                (5, 3, -8), (4, 4, -8), (3, 5, -8), (2, 6, -8), (1, 7, -8), (0, 8, -8), (-1, 9, -8), #I
                (5, 4, -9), (4, 5, -9), (3, 6, -9), (2, 7, -9), (1, 8, -9), (0, 9, -9) #J
                  ])

    self.occupied_list = {}
    self.no_play_tile = tuple()

    self.neibghbour_vectors = [(0,1,-1), #n
                        (0,-1,1), #s
                        (1,-1,0), #se
                        (-1,1,0), #nw
                        (-1,0,1), #sw
                        (1,0,-1)] #ne

  def win_check(self, coord): #untested
    curr_coord = coord
    color = self.occupied_list[coord]

    for vect in self.neibghbour_vectors:
      for i in range(4): #we need to find 4 neighbours to make 5 in row
        xi, yi, zi = coord
        new_coord = xi + vect[0], yi+ vect[1], zi + vect[2]

        if new_coord in self.occupied_list and self.occupied_list[new_coord] == color:
          curr_coord = new_coord
        else:
          break

        if i == 3:
          return True

    return False

  def capture_check(self, coord): #untested
    curr_coord = coord
    colors = []
    if self.occupied_list[coord] == "black":
      colors.extend(["white","white","black"])
    else:
      colors.extend(["black","black","white"])

    capture_choice = []
    for vect in self.neibghbour_vectors:
      xd, yd, zd = vect
      for i in range(3): #we need to find 4 neighbours to make a capture
        xi, yi, zi = curr_coord
        new_coord = xi + xd, yi + yd, zi + zd

        if new_coord in self.occupied_list and self.occupied_list[new_coord] == colors[i]:
          curr_coord = new_coord
        else:
          break
        if i == 3:
          x, y, z = coord
          capture_choice.append([(x + xd, y + yd, z + zd), (x + xd*2, y + yd*2), (z + zd*2)])

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

      # move tile from open to occupied
      self.open_coord.remove(coord)
      self.occupied_list[coord] = tile_color

      # check for win or captures
      win = self.win_check(coord)
      capture_choice = self.capture_check(coord)

    return win, capture_choice, illegal

  def capture_tile(self, tile):

    # move the tile from occupied to open
    del self.occupied_list[tile]
    self.open_coord.append(tile)

    # block the tile for the next play
    no_play_tile = tile

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