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
        self.player2 = game_agent.AlphaBetaPlayer()
        self.game = isolation.Board(self.player1, self.player2)

    def testInit(self):
        self.assertEqual(self.player1.TIMER_THRESHOLD, 10.)
        
    def testCustomScore(self):
        self.game.apply_move((2, 3))
        self.game.apply_move((1, 5))
        self.assertEqual(game_agent.custom_score_2(self.game, self.player1), 7)

    def testCustomScoreBeginning(self):
        self.assertEqual(game_agent.custom_score_2(self.game, self.player1), 49)

    def testTerminalState(self):
        self.game.apply_move((2, 3))
        self.game.apply_move((0, 5))
        self.assertEqual(self.player1.max_value(self.game, 0), 6)

if __name__ == '__main__':
    unittest.main()
