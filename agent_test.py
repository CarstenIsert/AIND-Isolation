"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import isolation
import game_agent
import competition_agent
from sample_players import open_move_score

from importlib import reload


class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)
        self.player1 = game_agent.MinimaxPlayer()
        self.player1.time_left = lambda: 15.
        self.player2 = game_agent.AlphaBetaPlayer()
        self.player2.time_left = lambda: 15.
        self.game = isolation.Board(self.player1, self.player2)

    def testInit(self):
        self.assertEqual(self.player1.TIMER_THRESHOLD, 11.)
        
    def testCustomScore(self):
        self.game.apply_move((2, 3))
        self.game.apply_move((1, 5))
        self.assertEqual(game_agent.custom_score(self.game, self.player1), 2.875)

    def testCustomScoreBeginning(self):
        self.assertEqual(game_agent.custom_score(self.game, self.player1), -18.375)

    def testMMTerminalStateScore(self):
        self.player1.score = open_move_score
        self.game.apply_move((2, 3))
        self.game.apply_move((0, 5))
        self.assertEqual(self.player1.max_value(self.game, 0), 8.0)

    def testMMDepth1Max(self):
        self.player1.score = open_move_score
        self.game.apply_move((2, 3))
        self.game.apply_move((0, 5))
        self.assertEqual(self.player1.max_value(self.game, 1), 7.0)

    def testMMDepth1Min(self):
        self.player1.score = open_move_score
        self.game.apply_move((2, 3))
        self.game.apply_move((0, 5))
        self.assertEqual(self.player1.min_value(self.game, 1), 3)

    def testMMDepth1Minimax(self):
        self.player1.score = open_move_score
        self.game.apply_move((2, 3))
        self.game.apply_move((0, 5))
        # As the moves are returned in random order and the evaluation selects the leftmost
        # node, we need to check the two best options.
        self.assertIn(self.player1.minimax(self.game, 1), [(4,4), (4,2)])

    def testABTerminalStateScore(self):
        self.player2.score = game_agent.custom_score
        self.game.apply_move((2, 3))
        self.game.apply_move((0, 5))
        self.assertEqual(self.player2.min_value(self.game, 0, float("-inf"), float("inf")), -8.0)

    def testABDepth1Min(self):
        self.player2.score = game_agent.custom_score
        self.game.apply_move((2, 3))
        self.game.apply_move((0, 5))
        self.game.apply_move((4, 2))
        self.assertEqual(self.player2.min_value(self.game, 1, float("-inf"), float("inf")), -6.625)

    def testABDepth1Max(self):
        self.player2.score = game_agent.custom_score
        self.game.apply_move((2, 3))
        self.game.apply_move((0, 5))
        self.game.apply_move((4, 2))
        self.assertEqual(self.player2.max_value(self.game, 1, float("-inf"), float("inf")), -2.625)

    def testABDepth1Alphabeta(self):
        self.player2.score = game_agent.custom_score
        self.game.apply_move((2, 3))
        self.game.apply_move((0, 5))
        self.game.apply_move((4, 2))
        self.assertEqual(self.player2.alphabeta(self.game, 1, float("-inf"), float("inf")), (2, 4))

class CompetitionTest(unittest.TestCase):
    def setUp(self):
        reload(competition_agent)
        self.player1 = competition_agent.CustomPlayer()
        self.player1.time_left = lambda: 15.
        self.player2 = game_agent.AlphaBetaPlayer()
        self.player2.time_left = lambda: 15.
        self.game = isolation.Board(self.player1, self.player2)
  
    def testInit(self): 
        self.assertEqual(self.player1.TIMER_THRESHOLD, 1.)

    def testFirstMoveOnEmptyBoard(self):
        self.assertEqual(self.player1.get_move(self.game, lambda: 15.), (3,3))
        
    def testSecondMoveToCenter(self):
        self.game.apply_move((1,1))
        self.assertEqual(self.player1.get_move(self.game, lambda: 15.), (3,3))
        
    def testSecondMoveCenterOccupied(self):
        self.game.apply_move((3,3))
        self.assertEqual(self.player1.get_move(self.game, lambda: 15.), (2,2))
    
    def testVerticalSymmetry(self):
        self.game.apply_move((1,1))
        self.game.apply_move((3,2))
        game_mirror = isolation.Board(self.player1, self.player2)
        game_mirror.apply_move((1,5))
        game_mirror.apply_move((3,4))
        game_horizontal_mirror = isolation.Board(self.player1, self.player2)
        game_horizontal_mirror.apply_move((5,1))
        game_horizontal_mirror.apply_move((3,2))
        (vertical_mirror_result, horizontal_mirror_result) = self.game.symmetric_configurations()
        self.assertEqual(vertical_mirror_result[0:49], game_mirror._board_state[0:49])
        self.assertEqual(horizontal_mirror_result[0:49], game_horizontal_mirror._board_state[0:49])
            

if __name__ == '__main__':
    unittest.main()
