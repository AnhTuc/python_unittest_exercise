import unittest
from unittest import mock

from dev.helper import *

class TestHelper(unittest.TestCase):

    @mock.patch("builtins.print")
    def test_game_over(self, fake_print):
        side_effects = [1000, 1034, 30, 10]
        player_score = mock.Mock(side_effect=side_effects)
        self.assertTrue(check_game_over(player_score()))
        self.assertTrue(check_game_over(player_score()))
        self.assertFalse(check_game_over(player_score()))
        self.assertTrue(check_game_over(player_score()))

    def test_process_input(self):
        side_effects = ['s','cot','continue','stop']
        user = mock.Mock(side_effect=side_effects)

        possible_inputs = ['continue','stop']
        self.assertEqual(process_input(user(), possible_inputs),'stop')
        self.assertEqual(process_input(user(), possible_inputs),'cot')
        self.assertEqual(process_input(user(), possible_inputs),'continue')
        self.assertEqual(process_input(user(), possible_inputs),'stop')

    @mock.patch("builtins.print")
    def test_handle_exception(self, mock_print):
        func = mock.Mock(side_effect=[KeyboardInterrupt, SystemExit, SyntaxError])
        with mock.patch('sys.exit') as fake_sys:
            handle_exception(func)()
            fake_sys.assert_called()
            handle_exception(func)()
            fake_sys.assert_called()
            handle_exception(func)()
            fake_sys.assert_called()
        

if __name__ =="__main__":
    unittest.main()