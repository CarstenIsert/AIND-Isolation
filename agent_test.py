"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import isolation
import game_agent

from importlib import reload


class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        print("Setup")
        reload(game_agent)
        self.player1 = game_agent.MinimaxPlayer()
        self.player1.time_left = lambda: 15.
        self.player2 = game_agent.AlphaBetaPlayer()
        self.player2.time_left = lambda: 15.
        self.game = isolation.Board(self.player1, self.player2)

    def testInit(self):
        self.assertEqual(self.player1.TIMER_THRESHOLD, 10.)
        
    def testCustomScore2(self):
        self.game.apply_move((2, 3))
        self.game.apply_move((1, 5))
        self.assertEqual(game_agent.custom_score_2(self.game, self.player1), 7)

    def testCustomScoreBeginning(self):
        self.assertEqual(game_agent.custom_score_2(self.game, self.player1), 49)

    def testMMTerminalStateScore(self):
        self.player1.score = game_agent.custom_score_2
        self.game.apply_move((2, 3))
        self.game.apply_move((0, 5))
        self.assertEqual(self.player1.max_value(self.game, 0), 8)

    def testMMDepth1Max(self):
        self.player1.score = game_agent.custom_score_2
        self.game.apply_move((2, 3))
        self.game.apply_move((0, 5))
        self.assertEqual(self.player1.max_value(self.game, 1), 7)

    def testMMDepth1Min(self):
        self.player1.score = game_agent.custom_score_2
        self.game.apply_move((2, 3))
        self.game.apply_move((0, 5))
        self.assertEqual(self.player1.min_value(self.game, 1), 3)

    def testMMDepth1Minimax(self):
        self.player1.score = game_agent.custom_score_2
        self.game.apply_move((2, 3))
        self.game.apply_move((0, 5))
        # As the moves are returned in random order and the evaluation selects the leftmost
        # node, we need to check the two best options.
        self.assertIn(self.player1.minimax(self.game, 1), [(4,4), (4,2)])

    def testABTerminalStateScore(self):
        self.player2.score = game_agent.custom_score_2
        self.game.apply_move((2, 3))
        self.game.apply_move((0, 5))
        self.assertEqual(self.player2.min_value(self.game, 0, float("-inf"), float("inf")), 3)

    def testABDepth1Min(self):
        self.player2.score = game_agent.custom_score_2
        self.game.apply_move((2, 3))
        self.game.apply_move((0, 5))
        self.game.apply_move((4, 2))
        self.assertEqual(self.player2.min_value(self.game, 1, float("-inf"), float("inf")), 3)

    def testABDepth1Max(self):
        self.player2.score = game_agent.custom_score_2
        self.game.apply_move((2, 3))
        self.game.apply_move((0, 5))
        self.game.apply_move((4, 2))
        self.assertEqual(self.player2.max_value(self.game, 1, float("-inf"), float("inf")), 7)

    def testABDepth1Alphabeta(self):
        self.player2.score = game_agent.custom_score_2
        self.game.apply_move((2, 3))
        self.game.apply_move((0, 5))
        self.game.apply_move((4, 2))
        self.assertEqual(self.player2.alphabeta(self.game, 1, float("-inf"), float("inf")), (2, 4))


if __name__ == '__main__':
    unittest.main()
