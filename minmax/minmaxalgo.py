"""module containing the minmax algorithms"""

from random import choice

from bokuboard.bokulogic import BokuGame

# TODO account for captures
# TODO Iterative deepening

def ab_negmax_random_capture(node: BokuGame,
                             depth: int,
                             alpha: int=float('-inf'),
                             beta: int=float('inf')):
    """negamax algorithm with alpha beta pruning"""

    ## Base Case: check if we are at a leaf node
    # recusion depth is is reached or the game is over (win, lose, draw)
    if depth == 0 or node.heuristic["winner"] != "":
        # the board reports the value according to white's perspective
        value = node.eval() if len(node.history) % 2 == 0 else -node.eval()
        return node.history[-1][0], value

    ## Recursion Case:
    # initialize the best move, score and the color of the player to play
    score = float('-inf')
    best_move = None
    color = "white" if len(node.history) % 2 == 0 else "black"

    # go through all the children (moves) by iterating the move order priorityq
    for move in node.heuristic["move order"]:
        # skip the no play tile, this is the only illegal move in the priorityq
        # because the priorityq is shared between the two players
        if move.tile == node.no_play_tile:
            continue

        # play the move (generate the successor state)
        #TODO a win can be detected here, should it?
        _, _, capture_choice = node.play_tile(move.tile, color)

        # check if there is a capture
        if capture_choice:
            # randomly capture
            capture = choice(list(capture_choice))
            node.play_capture(capture, capture_choice)

        # call negamax on the successor state, flip the signs
        _, value = ab_negmax_random_capture(node, depth - 1, -beta, -alpha)
        value *= -1

        # undo the move, so we only ever use one BokuGame object
        node.undo()

        if value > score:
            score = value
            best_move = move.tile

        if score > alpha:
            alpha = score

        if score >= beta:
            break

    return best_move, score
