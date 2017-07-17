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
        self.player1 = game_agent.MinimaxPlayer
        self.player2 = "Player2"
        self.game = isolation.Board(self.player1, self.player2)

    def testTerminalState(self):
        self.assertEqual(self.player1.max_value(self, self.game, 0), 6)


if __name__ == '__main__':
    unittest.main()
