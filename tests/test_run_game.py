import sys
import os
sys.path.append(os.getcwd())
import unittest
from unittest import mock
from dev import main
from dev.card_game import CardGame
from dev.player import Player
from dev import helper
import logging


class TestRun(unittest.TestCase):
    def setUp(self) -> None:
        self.player1 = Player(player_score=60, name='abc')
        self.game = CardGame()
    """
    Failed test in group of try and except
    """

    @mock.patch("builtins.input")
    @mock.patch("builtins.print")
    def test_game_continue_exit(self, fake_print, fake_input):
        """
        Test return if game continue, when testing remember to comment the try and except block as os.exit
        """
        helper.process_input = mock.Mock(return_value='stop')
        helper.check_game_over = mock.Mock(return_value=False)

        main.game_continue(house = self.game, player=self.player1)
        self.assertRaises(SystemExit)
            #fake_print.assert_called_with("Closing card game ...")
            # self.assertEqual(cm.exception.code, 1)

    @mock.patch("builtins.print")
    @mock.patch("builtins.input")
    def test_game_continue_retrieve(self, fake_input, fake_print):
        """
        Test return if game continue
        dev.helper(print(input((test)))
        """

        fake_input.return_value = 'dsfbg'
        helper.process_input = mock.MagicMock(return_value='sgsd')
        helper.check_game_over = mock.MagicMock(return_value = False)

        with mock.patch('dev.main.card_game') as fake_game:
            main.game_continue(house=self.game, player = self.player1)
            fake_print.assert_called_with("Retrieve game ...\n"+"."*20)
            fake_game.assert_called()
    

    @mock.patch("builtins.input")
    @mock.patch("builtins.print")
    @mock.patch("dev.helper")
    def test_game_continue_retrieve2(self, fake_helper,fake_print,fake_input):
        """
        Test return if game continue
        dev.helper(print(input((test)))
        """

        fake_input.return_value = 'dsfbg'
        fake_helper.process_input.return_value = 'hgf'
        fake_helper.check_game_over.return_value = False

        with mock.patch('dev.main.card_game') as fake_game:
            main.game_continue(house=self.game, player = self.player1)
            fake_print.assert_called_with("Retrieve game ...\n"+"."*20)
            fake_game.assert_called()
    


    @mock.patch("builtins.print")
    def test_card_game_exception(self, fake_print):
        """
        Test card game handling exception
        """
        main.game_continue = mock.Mock()
        
        with mock.patch.object(CardGame,'start_game') as fake_game:
            fake_game.side_effect = [KeyboardInterrupt, EOFError]
            main.card_game(player_name = 'test game')
            self.assertLogs("\nKeyboard Interrupt: Closing Card game?", level =logging.WARNING)
            main.game_continue.assert_called()
            main.card_game(player_name = 'test game')
            self.assertLogs("\nError Approach. Closing Card game.",level =logging.WARNING)
    



if __name__ == "__main__":
    unittest.main()