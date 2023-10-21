"""module containing the minmax algorithms"""

from random import choice

from bokuboard.bokulogic import BokuGame

def ab_negmax_random_capture(node: BokuGame,
                             depth: int,
                             alpha: int=float('-inf'),
                             beta: int=float('inf')):
    """negamax algorithm with alpha beta pruning"""

    # Base Case: check if we are at a leaf node
    # curusion depth is is reached or the game is over (win, lose, draw)
    if depth == 0 or node.heuristic["winner"] != "":
        # the board reports the value according to white's perspective
        value = node.eval() if len(node.history) % 2 == 0 else -node.eval()
        return node.history[-1][0], value
    score = float('-inf')
    best_move = None

    # get the color of the player to play
    color = "white" if len(node.history) % 2 == 0 else "black"

    # go through all the children (moves) by iterating the move order priorityq
    for move in node.heuristic["move order"]:
        # skip the no play tile, this is the only illegal move in the priorityq
        # because the priorityq is shared between the two players
        if move.tile == node.no_play_tile:
            continue

        # play the move (generate the successor state)
        node._place_tile(move.tile, color)

        # run heuristic check to see if there is a capture
        #TODO a win can be detected here, should it?
        _, capture_choice = node._win_capture_check(move.tile, color, True)

        # check if there is a capture
        if capture_choice:
            # randomly capture
            capture = choice(list(capture_choice))
            node.capture_tile(capture)

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
