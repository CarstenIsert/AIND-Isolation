"""This file contains a collection of player classes for comparison with your
own agent and example heuristic functions.

    ************************************************************************
    ***********  YOU DO NOT NEED TO MODIFY ANYTHING IN THIS FILE  **********
    ************************************************************************
"""

from random import randint
from random import choice

import game_agent
import timeit
import json
import isolation
import os.path

def null_score(game, player):
    """This heuristic presumes no knowledge for non-terminal states, and
    returns the same uninformative value for all other states.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return 0.


def open_move_score(game, player):
    """The basic evaluation function described in lecture that outputs a score
    equal to the number of moves open for your computer player on the board.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return float(len(game.get_legal_moves(player)))


def improved_score(game, player):
    """The "Improved" evaluation function discussed in lecture that outputs a
    score equal to the difference in the number of moves available to the
    two players.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - opp_moves)


def center_score(game, player):
    """Outputs a score equal to square of the distance from the center of the
    board to the position of the player.

    This heuristic is only used by the autograder for testing.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    w, h = game.width / 2., game.height / 2.
    y, x = game.get_player_location(player)
    return float((h - y)**2 + (w - x)**2)


class RandomPlayer():
    """Player that chooses a move randomly."""

    def get_move(self, game, time_left):
        """Randomly select a move from the available legal moves.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        ----------
        (int, int)
            A randomly selected legal move; may return (-1, -1) if there are
            no available legal moves.
        """
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return (-1, -1)
        return legal_moves[randint(0, len(legal_moves) - 1)]


class GreedyPlayer():
    """Player that chooses next move to maximize heuristic score. This is
    equivalent to a minimax search agent with a search depth of one.
    """

    def __init__(self, score_fn=open_move_score):
        self.score = score_fn

    def get_move(self, game, time_left):
        """Select the move from the available legal moves with the highest
        heuristic score.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        ----------
        (int, int)
            The move in the legal moves list with the highest heuristic score
            for the current game state; may return (-1, -1) if there are no
            legal moves.
        """
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return (-1, -1)
        _, move = max([(self.score(game.forecast_move(m), self), m) for m in legal_moves])
        return move


class HumanPlayer():
    """Player that chooses a move according to user's input."""

    def get_move(self, game, time_left):
        """
        Select a move from the available legal moves based on user input at the
        terminal.

        **********************************************************************
        NOTE: If testing with this player, remember to disable move timeout in
              the call to `Board.play()`.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        ----------
        (int, int)
            The move in the legal moves list selected by the user through the
            terminal prompt; automatically return (-1, -1) if there are no
            legal moves
        """
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return (-1, -1)

        print(game.to_string()) #display the board for the human player
        print(('\t'.join(['[%d] %s' % (i, str(move)) for i, move in enumerate(legal_moves)])))

        valid_choice = False
        while not valid_choice:
            try:
                index = int(input('Select move index:'))
                valid_choice = 0 <= index < len(legal_moves)

                if not valid_choice:
                    print('Illegal move! Try again.')

            except ValueError:
                print('Invalid index! Try again.')

        return legal_moves[index]


if __name__ == "__main__":
    from isolation import Board

    # create an isolation board (by default 7x7)
    player1 = game_agent.AlphaBetaPlayer()
    player2 = GreedyPlayer()
    game = Board(player1, player2)
    time_millis = lambda: 1000 * timeit.default_timer()

    # TODO: Move code to CustomPlayer
    # TODO: Gernate large version of opening book
    # TODO: Make opening book storage, loading etc. more efficient
    if os.path.exists('data.json'):
        with open('data.json', 'rb') as data_fp:
            opening_book = json.load(data_fp)
            data_fp.close()
    else:
        opening_book = {}
    
    # Initialize the board with two random moves for each player.
#    for _ in range(2):
#        move = choice(game.get_legal_moves())
#        game.apply_move(move)
    game.apply_move((5, 1))
    game.apply_move((3, 4))
    
    for i in range(10):
        move_start = time_millis()
        time_left = lambda : 2000 - (time_millis() - move_start)

        sym = [0,1,2,3,4,5,6,7]
        sym[0] = game._board_state[0:49]
        print("Current board: ", str(sym[0]))
        (sym[1], sym[2], sym[3], sym[4], sym[5], sym[6], sym[7]) = game.symmetric_configurations()
    
        # Check if symmetric configs are in the opening book
        move = (-1,-1)
        for config in sym:
            hash_config = str(str(config).__hash__())
            print("Hash: ", hash_config)
            if hash_config in opening_book:
                (move_list, sym) = opening_book[hash_config]
                move = tuple(move_list)
                print("Found move in opening book", move)
        
        if move == (-1, -1):
            move = player1.get_move(game, time_left)
            print("Adding this move to the opening book: ", sym[0], ":", move)
            # TODO: Need to store the type of symmetry to be able to mirror the move back!
            opening_book[game.hash()] = (move, 0)
        
        move_end = time_left()

        game.apply_move(move)

    print("Writing new version of opening book.")
    with open('data.json', 'w') as data_fp:
        json.dump(opening_book, data_fp)
        data_fp.close()
    
    # place player 1 on the board at row 2, column 3, then place player 2 on
    # the board at row 0, column 5; display the resulting board state.  Note
    # that the .apply_move() method changes the calling object in-place.
    #game.apply_move((2, 3))
    #game.apply_move((1, 5))
    #print(game.to_string())

    # players take turns moving on the board, so player1 should be next to move
    #assert(player1 == game.active_player)

    # play the remainder of the game automatically -- outcome can be "illegal
    # move", "timeout", or "forfeit"
    #winner, history, outcome = game.play()
    #print("\nWinner: {}\nOutcome: {}".format(winner, outcome))
    #print(game.to_string())
    #print("Move history:\n{!s}".format(history))
