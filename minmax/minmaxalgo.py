"""module containing the minmax algorithms"""

from random import choice

from bokuboard.bokulogic import BokuGame

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
        _, win, capture_choice = node.play_tile(move.tile, color)

        # check for a win, skip into Base Case
        if win:
            # undo the move, so we only ever use one BokuGame object
            node.undo()

            # the board reports the value according to white's perspective
            value = node.eval() if len(node.history) % 2 == 0 else -node.eval()
            return move.tile, value

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

def ab_negmax_with_capture(node: BokuGame,
                             depth: int,
                             alpha: int=float('-inf'),
                             beta: int=float('inf')):
    """negamax algorithm with alpha beta pruning"""

    ## Base Case: check if we are at a leaf node
    # recusion depth is is reached or the game is over (win, lose, draw)
    if depth == 0 or node.heuristic["winner"] != "":
        # the board reports the value according to white's perspective
        value = node.eval() if len(node.history) % 2 == 0 else -node.eval()
        move = node.history[-1][0]
        capture = node.history[-1][1] if len(node.history[-1]) > 1 else None
        return move, capture, value

    ## Recursion Case:
    # initialize the best move, score and the color of the player to play
    score = float('-inf')
    best_move = None
    color = "white" if len(node.history) % 2 == 0 else "black"

    # go through all the children (moves) by iterating the move order priorityq
    for move in node.heuristic["move order"]:
        move_capture = None
        # skip the no play tile, this is the only illegal move in the priorityq
        # because the priorityq is shared between the two players
        if move.tile == node.no_play_tile:
            continue

        # play the move (generate the successor state)
        _, win, capture_choice = node.play_tile(move.tile, color)

        # check for a win, skip into Base Case
        if win:
            # undo the move, so we only ever use one BokuGame object
            node.undo()

            # the board reports the value according to white's perspective
            value = node.eval() if len(node.history) % 2 == 0 else -node.eval()
            return move.tile, move_capture, value

        # check if there is a capture
        if capture_choice:
            # iterate through the captures
            break_bool = False
            for capture in capture_choice:
                node.play_capture(capture, capture_choice)

                # call negamax encapsulated logic for each capture
                break_bool, alpha, beta, score, best_move, move_capture = ab_negmax_score_logic(node, depth, alpha, beta, score, best_move, move, capture)

                if break_bool:
                    break

            # undo the move
            node.undo()

            if break_bool:
                break

        else:
            # call negamax encapsulated logic
            break_bool, alpha, beta, score, best_move, move_capture = ab_negmax_score_logic(node, depth, alpha, beta, score, best_move, move, None)

            if break_bool:
                break

    return best_move, move_capture, score

def ab_negmax_score_logic(node, depth, alpha, beta, score, best_move, move, capture):
    """negamax algorithm value update logic"""
    break_bool = False
    move_capture = None
    # TODO pass a dict reference for all the variables that need to be updated

    # call negamax on the successor state, flip the signs
    _, _, value = ab_negmax_with_capture(node, depth - 1, -beta, -alpha)
    value *= -1

    # undo the move, so we only ever use one BokuGame object
    if capture is None:
        # undo the whole move
        node.undo()
    else:
        # undo just the capture
        node.history[-1].remove(capture)

    if value > score:
        score = value
        best_move = move.tile
        move_capture = capture


    if score > alpha:
        alpha = score

    if score >= beta:
        break_bool = True

    return break_bool, alpha, beta, score, best_move, move_capture
