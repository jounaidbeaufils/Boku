"""module containing the minmax algorithms"""

from bokuboard.bokulogic import BokuGame

def abnegmax(self, node: BokuGame, depth: int, alpha: int, beta: int):
    """negamax algorithm with alpha beta pruning"""
    # check if we are at a leaf node
    if depth == 0 or node.heuristic["winner"] is not None:
        return node.eval()
    v = float('inf')

    # get the color of the player to play
    color = "white" if len(node.history) % 2 == 0 else "black"

    # go through all the children (moves) by move order priorityq
    for move in node.heuristic["move order"]:
        node.place_tile(move.tile, color)
        v = min(v, self.annegmax(node, depth - 1, alpha, beta))
        if v <= alpha:
            # undo the move, this ensures that we only ever use one board
            node.undo()
            return v
        beta = min(beta, v)

    # undo the move, this ensures that we only ever use one board
    node.undo()
    return v
