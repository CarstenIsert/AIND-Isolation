"""Implement your own custom search agent using any combination of techniques
you choose.  This agent will compete against other students (and past
champions) in a tournament.

         COMPLETING AND SUBMITTING A COMPETITION AGENT IS OPTIONAL
"""
import random
import math

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    moves_own = len(game.get_legal_moves(player))
    moves_opp = len(game.get_legal_moves(game.get_opponent(player)))
    board_size = game.height * game.width
    moves_placed_ratio = game.move_count / board_size
    if moves_placed_ratio > 0.33:
        move_diff = (moves_own - moves_opp*2) 
    else:
        move_diff = (moves_own - moves_opp)

    pos_own = game.get_player_location(player)
    pos_opp = game.get_player_location(game.get_opponent(player))

    m_distance = abs(pos_own[0] - pos_opp[0]) + abs(pos_own[1] - pos_opp[1])

    return float(move_diff / m_distance)
    raise NotImplementedError


class CustomPlayer:
    """Game-playing agent to use in the optional player vs player Isolation
    competition.

    You must at least implement the get_move() method and a search function
    to complete this class, but you may use any of the techniques discussed
    in lecture or elsewhere on the web -- opening books, MCTS, etc.

    **************************************************************************
          THIS CLASS IS OPTIONAL -- IT IS ONLY USED IN THE ISOLATION PvP
        COMPETITION.  IT IS NOT REQUIRED FOR THE ISOLATION PROJECT REVIEW.
    **************************************************************************

    Parameters
    ----------
    data : string
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted.  Note that
        the PvP competition uses more accurate timers that are not cross-
        platform compatible, so a limit of 1ms (vs 10ms for the other classes)
        is generally sufficient.
    """

    def __init__(self, data=None, timeout=1.):
        self.score = custom_score
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def check_timing(self):
        """ To avoid code duplication the time checking should be done in a consistent way
        in the base class so that all derived algorithms can use the same functions.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
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
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        
        self.time_left = time_left

        # TODO: If we are in the beginning stage of the game
        # TODO: First check about symmetry
        # TODO: Look up opening book for best move
        if game.move_count == 0:
            return (3,3)
        
        if game.move_count == 1:
            if game.move_is_legal((3,3)):
              return (3,3)
            else:
              return (2,2)
            
        
        try:
            iterative_depth = 1
            max_depth = 25
    
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            while iterative_depth <= max_depth:
                best_move = self.alphabeta(game, iterative_depth, float("-inf"), float("inf"))
                iterative_depth += 1

        except SearchTimeout:
            return best_move

        return best_move

    def min_value(self, game, current_depth, alpha, beta):
        self.check_timing()

        legal_moves = game.get_legal_moves()

        if (current_depth <= 0) or (not legal_moves):
            return self.score(game, self)

        if game.utility(self) != 0.0:
            return game.utility(self)
        
        min_score = math.inf
        current_beta = beta
        for move in legal_moves:
            result_game = game.forecast_move(move)
            current_score = self.max_value(result_game, current_depth - 1, alpha, current_beta)
            if current_score < min_score:
                min_score = current_score
            if min_score <= alpha:
                return min_score
            current_beta = min(current_beta, min_score)

        return min_score
      
    def max_value(self, game, current_depth, alpha, beta):
        self.check_timing()

        legal_moves = game.get_legal_moves()

        if (current_depth <= 0) or (not legal_moves):
            return self.score(game, self)

        if game.utility(self) != 0.0:
            return game.utility(self)
        
        max_score = -math.inf
        current_alpha = alpha
        for move in legal_moves:
            result_game = game.forecast_move(move)
            current_score = self.min_value(result_game, current_depth - 1, current_alpha, beta)
            if current_score > max_score:
                max_score = current_score
            if max_score >= beta:
                return max_score
            current_alpha = max(current_alpha, max_score)

        return max_score

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        self.check_timing()

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return (-1, -1)
          
        if depth < 1:
            return legal_moves[0]
       
        # As we have legal moves and might timeout anytime, it is better to select
        # an arbitrary first move than an invalid move.
        max_move = legal_moves[0]
        max_score = -math.inf  
        current_alpha = alpha
        for move in legal_moves:
            result_game = game.forecast_move(move)
            current_score = self.min_value(result_game, depth - 1, current_alpha, beta)
            if current_score > max_score:
                max_move = move
                max_score = current_score
            if max_score >= beta:
                break
            current_alpha = max(current_alpha, max_score)
        
        return max_move
        
