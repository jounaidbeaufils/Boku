"""module for displaying the board"""
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
from bokuboard import bokudata

from bokuboard.bokulogic import BokuGame

def draw_board(game: BokuGame):
    """draw the board"""

    colors = [game.occupied_dict.get(tuple(c), "blue") for c in bokudata.all_coords]
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
        ax.text(x, y, bokudata.centricity_values[coord], ha='center', va='center', fontsize=10)

    # add scatter points in hexagon centers, to ensure all hexagons are in the plot zoom range
    # TODO !fix this ploting hack
    ax.scatter(hcoord, vcoord, alpha=0.0)

    plt.show(block=False)

if __name__ == "__main__":
    game = BokuGame()
    draw_board(game)
    input("press enter to continue")