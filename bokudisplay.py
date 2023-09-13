import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import RegularPolygon

from bokulogic import BokuGame

def draw_board(occupied):
  coord = [(0,0,0), (-1,1,0), (-2,2,0), (-3,3,0), (-4,4,0), (-5,5,0), #A
           (1,0,-1), (0,1,-1), (-1,2,-1), (-2,3,-1), (-3,4,-1), (-4,5,-1), (-5,6,-1), #B
           (2, 0, -2), (1, 1, -2), (0, 2, -2), (-1, 3, -2), (-2, 4, -2), (-3, 5, -2), (-4, 6, -2), (-5, 7, -2), #C
           (3, 0, -3), (2, 1, -3), (1, 2, -3), (0, 3, -3), (-1, 4, -3), (-2, 5, -3), (-3, 6, -3), (-4, 7, -3), (-5, 8, -3), #D
           (4, 0, -4), (3, 1, -4), (2, 2, -4), (1, 3, -4), (0, 4, -4), (-1, 5, -4), (-2, 6, -4), (-3, 7, -4), (-4, 8, -4), (-5, 9, -4), #E
           (5, 0, -5), (4, 1, -5), (3, 2, -5), (2, 3, -5), (1, 4, -5), (0, 5, -5), (-1, 6, -5), (-2, 7, -5), (-3, 8, -5), (-4, 9, -5), #F
           (5, 1, -6), (4, 2, -6), (3, 3, -6), (2, 4, -6), (1, 5, -6), (0, 6, -6), (-1, 7, -6), (-2, 8, -6), (-3, 9, -6), #G
           (5, 2, -7), (4, 3, -7), (3, 4, -7), (2, 5, -7), (1, 6, -7), (0, 7, -7), (-1, 8, -7), (-2, 9, -7), #H
           (5, 3, -8), (4, 4, -8), (3, 5, -8), (2, 6, -8), (1, 7, -8), (0, 8, -8), (-1, 9, -8), #I
           (5, 4, -9), (4, 5, -9), (3, 6, -9), (2, 7, -9), (1, 8, -9), (0, 9, -9) #J
          ]
  colors = [occupied.get(tuple(c), "blue") for c in coord]

  # Horizontal cartesian coords
  hcoord = [c[0] for c in coord]

  # Vertical cartesian coords
  vcoord = [2. * np.sin(np.radians(60)) * (c[1] - c[2]) / 3. for c in coord]

  fig, ax = plt.subplots(1, figsize=(10, 10))
  ax.set_aspect('equal')

  # Add some colored hexagons and labels
  for x, y, color, (xi, yi, zi) in zip(hcoord, vcoord, colors, coord):
    hexagon = RegularPolygon((x, y), numVertices=6, radius=2. / 3,
                              orientation=np.radians(30), facecolor=color,
                              alpha=0.3, edgecolor='k')
    ax.add_patch(hexagon)
    ax.text(x, y, BokuGame.coord_to_notation(xi,yi,zi), ha='center', va='center', fontsize=10)

  # Also add scatter points in hexagon centers
  ax.scatter(hcoord, vcoord, alpha=0.0)

  plt.show()

if __name__ == "__main__":
  occupied = {(-2,6,-4):"white",
              (0,6,-6):"black"}

  draw_board(occupied)