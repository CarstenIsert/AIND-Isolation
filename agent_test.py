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

    def testOccupyFirstMove(self):
        self.player1.occupy_start_position(self.game)
        self.assertEqual((3,3), self.player1.best_move)
    
    def testSymmetry(self):
        self.game.apply_move((1,1))
        self.game.apply_move((3,2))
        
        game_vertical = isolation.Board(self.player1, self.player2)
        game_vertical.apply_move((1,5))
        game_vertical.apply_move((3,4))
        
        game_horizontal = isolation.Board(self.player1, self.player2)
        game_horizontal.apply_move((5,1))
        game_horizontal.apply_move((3,2))
        
        game_rotation90 = isolation.Board(self.player1, self.player2)
        game_rotation90.apply_move((1,5))
        game_rotation90.apply_move((2,3))

        game_rotation180 = isolation.Board(self.player1, self.player2)
        game_rotation180.apply_move((5,5))
        game_rotation180.apply_move((3,4))
        
        game_rotation270 = isolation.Board(self.player1, self.player2)
        game_rotation270.apply_move((5,1))
        game_rotation270.apply_move((4,3))

        game_diag1 = isolation.Board(self.player1, self.player2)
        game_diag1.apply_move((5,5))
        game_diag1.apply_move((4,3))
        
        game_diag2 = isolation.Board(self.player1, self.player2)
        game_diag2.apply_move((1,1))
        game_diag2.apply_move((2,3))
        
        [_, vertical, horizontal, rotation90, rotation180, rotation270, diag1, diag2] = self.game.symmetric_configurations()

        self.assertEqual(vertical[0:49], game_vertical._board_state[0:49])
        self.assertEqual(horizontal[0:49], game_horizontal._board_state[0:49])
        self.assertEqual(rotation90[0:49], game_rotation90._board_state[0:49])
        self.assertEqual(rotation180[0:49], game_rotation180._board_state[0:49])
        self.assertEqual(rotation270[0:49], game_rotation270._board_state[0:49])
        self.assertEqual(diag1[0:49], game_diag1._board_state[0:49])
        self.assertEqual(diag2[0:49], game_diag2._board_state[0:49])
            
    def testOpeningBook(self):
        self.player1.load_opening_book('test.json')
        (move_list, sym) = self.player1.opening_book['-2930664380439188361']
        move = tuple(move_list)
        self.assertEqual(move, (3,0))
        self.assertEqual(competition_agent.Symmetries(sym), competition_agent.Symmetries.SAME)
        
    def testInitCustomPlayerWithBook(self):
        new_player = competition_agent.CustomPlayer('test.json')
        (move_list, sym) = new_player.opening_book['-2930664380439188361']
        move = tuple(move_list)
        self.assertEqual(move, (3,0))
        self.assertEqual(competition_agent.Symmetries(sym), competition_agent.Symmetries.SAME)
        
    def testInitCustomPlayerWithoutBook(self):
        new_player = competition_agent.CustomPlayer()
        self.assertEqual(new_player.opening_book, {})
        
    def testUpdateOpeningBook4Symmetries(self):
        self.game.apply_move((1,1))
        self.player1.best_move = (1,1)
        self.player1.update_opening_book(self.game)
        print(self.player1.opening_book)
        self.assertEqual(self.player1.opening_book['-8974553412868527889'], ((1,1), competition_agent.Symmetries.SAME.value))
        self.assertEqual(len(self.player1.opening_book), 4)
    
    def testUpdateOpeningBook8Symmetries(self):
        self.game.apply_move((1,1))
        self.game.apply_move((3,2))
        self.player1.best_move = (3,2)
        self.player1.update_opening_book(self.game)
        print(self.player1.opening_book)
        self.assertEqual(self.player1.opening_book['5105712017171821632'], ((3,2), competition_agent.Symmetries.SAME.value))
        self.assertEqual(len(self.player1.opening_book), 8)

    def testRotateMove1(self):
        self.assertEqual(self.player1.backrotate_move([2,2], competition_agent.Symmetries.VERTICAL), (2, 4))
           
    def testRotateMove2(self):
        self.assertEqual(self.player1.backrotate_move([2,2], competition_agent.Symmetries.HORIZONTAL), (4, 2))
           
    def testRotateMove3(self):
        self.assertEqual(self.player1.backrotate_move([2,2], competition_agent.Symmetries.ROTATE90), (4, 2))
           
    def testRotateMove4(self):
        self.assertEqual(self.player1.backrotate_move([2,2], competition_agent.Symmetries.ROTATE180), (4, 4))
           
    def testRotateMove5(self):
        self.assertEqual(self.player1.backrotate_move([2,2], competition_agent.Symmetries.ROTATE270), (2, 4))
           
    def testRotateMove6(self):
        self.assertEqual(self.player1.backrotate_move([2,2], competition_agent.Symmetries.DIAG1), (4, 4))
           
    def testRotateMove7(self):
        self.assertEqual(self.player1.backrotate_move([2,2], competition_agent.Symmetries.DIAG2), (2, 2))
           


if __name__ == '__main__':
    unittest.main()
