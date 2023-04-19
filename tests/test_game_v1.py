import sys
sys.path.append("D:\\PythonExame\\dev")

import logging

from dev.card_game import CardGame
from dev.player import Player
from dev.deck import Deck
import unittest
from unittest import mock
from dev.helper import *


class TestGame(unittest.TestCase):
    def setUp(self):
        player = Player(player_score = 60, name ='abc')
        self.game = CardGame(player, reward = 20, cost =30)

    def test_deal_card(self):
        """
        Test if host and player each has a card
        """
       
        #self.assertEqual(self.game.deck.size,52)
        self.assertIsNone(self.game.card)
        self.assertIsNone(self.game.player.card)
        self.game.deal_card()
        self.assertIsNotNone(self.game.card)
        self.assertIsNotNone(self.game.player.card)
    
    def test_card_info(self):
        side_effects = [
            {'value':"Ace",'suit':"Spades"}, {'value':"2",'suit':"Spades"},
            # 2nd game
            {'value':"King",'suit':"Diamonds"}, {'value': "8",'suit':"Hearts"}
        ]
        card = mock.Mock(side_effect=side_effects)
        self.assertEqual(self.game.get_card_info(card()),'A\u2660')
        self.assertEqual(self.game.get_card_info(card()),'2\u2660')
        self.assertEqual(self.game.get_card_info(card()),'K\u2666')
        self.assertEqual(self.game.get_card_info(card()),'8\u2665')

    @mock.patch("builtins.print")
    def test_reveal_card(self, fake_print):
        """
        Test if the house card is reveal correctly
        """
        # side_effects = [
        #     Stack(cards = [Card("Ace","Spades")]),
        #     Stack(cards = [Card("2","Heart")])
        # ]

        # # game = CardGame()
        # self.game.deck.deal = mock.Mock(side_effect = side_effects)
        self.game.deal_card()
        # self.game.house.card = mock.Mock(return_value ={'value':'Ace', 'suit':"Spades"})
        with mock.patch.dict(self.game.card,{'value':'Ace', 'suit':'Spades'}) as fake_card:
            self.game.reveal_card(fake_card)
            fake_print.assert_any_call("House has A\u2660")
            
            #After reveal --> card is put back to the deck
            self.assertIsNone(fake_card)

    #Mock patch replace target with a mock object
    @mock.patch("builtins.print")
    def test_player_guess(self,fake_print):
        """
        Test player's guess format
        """
        input_side_effects = ['l','h','x','higher']
        possible_inputs = ['higher','lower']
        with mock.patch("builtins.input", side_effect=input_side_effects) as fake_input:
            # game = CardGame()
            self.game.card = {'value':'Ace', 'suit':'Spades'}
            guess = self.game.player_guess(possible_inputs)
            self.assertEqual(guess, "lower")
            guess = self.game.player_guess(possible_inputs)
            self.assertEqual(guess, "higher")
            guess = self.game.player_guess(possible_inputs)
            self.assertEqual(guess, "higher")
    
    def test_compare_card(self):
        """
        Test compare card
        """
        side_effects=[
           {'value':"Ace",'suit':"Spades"}, {'value':"2",'suit':"Spades"},
            # 2nd game
            {'value':"King",'suit':"Spades"}, {'value': "8",'suit':"Hearts"},
            # 3rd game
            {'value':"Ace",'suit':"Hearts"}, {'value':"King",'suit': "Clubs"},
            # 4th game
            {'value':"5",'suit': "Hearts"}, {'value':"5",'suit':"Diamonds"},
        ]

        deal = mock.Mock(side_effect=side_effects)
        result = self.game.compare_card(deal(1),deal(1))
        self.assertEqual(result,'higher')
        result = self.game.compare_card(deal(1),deal(1))
        self.assertEqual(result,'lower')
        result = self.game.compare_card(deal(1),deal(1))
        self.assertEqual(result,'higher')
        result = self.game.compare_card(deal(1),deal(1))
        self.assertEqual(result,'higher')

    @mock.patch("builtins.input")
    @mock.patch("builtins.print")
    def test_player_continue(self, fake_print, fake_inputs):
        fake_inputs.side_effect = ["c", "conTinue", "S", "sto", "Stop"]
        # game = CardGame()

        s_or_c = self.game.player_continue()
        self.assertEqual(s_or_c,'continue')
        s_or_c = self.game.player_continue()
        self.assertEqual(s_or_c,'continue')
        s_or_c = self.game.player_continue()
        self.assertEqual(s_or_c,'stop')
        s_or_c = self.game.player_continue()
        self.assertLogs(logging.INFO)
        self.assertEqual(s_or_c,'stop')

    @mock.patch("builtins.input")
    @mock.patch("builtins.print")
    def test_start_match(self, fake_print, fake_input):
        side_effects = [
            {'value':"Ace",'suit':"Spades"}, {'value':"2",'suit':"Spades"},
            # 2nd game
            {'value':"King",'suit':"Spades"}, {'value': "8",'suit':"Hearts"},
        ]

        fake_input.side_effect = ['higher','lg','lower']

        with mock.patch.object('dev.deck.Deck', 'deck_deal') as fake_deck:
            fake_deck.side_effect = side_effects
            guess, result = self.game.start_match()
            self.assertEqual(guess,'higher')
            self.assertEqual(result,'lower')

            guess, result = self.game.start_match()
            self.assertEqual(guess,'lower')
            self.assertEqual(result,'lower')

    @mock.patch('builtins.input')
    def test_play_match(self, fake_input):
        side_effects =[('lower','lower'),('higher','higher'),('lower','higher')]
        self.game.start_match = mock.Mock(side_effect=side_effects)

        fake_input.side_effect =['c','c','so','c']
        
        with mock.patch('builtins.print') as fake_print:
            self.game.play_match()
            self.assertEqual(self.game.player.score,60)

            # self.player_continue = mock.Mock(side_effect=['True','False','False'])
            # fake_input.side_effect =['c','s']
            # self.game.play_match()
            # self.assertEqual(self.game.player,70)

    
    # def test_return_card(self):
    #     """
    #     Test card return after deal
    #     """
    #     self.assertEqual(self.game.deck.size,52)
    #     self.game.deal_card()
    #     tmp_house_card = "%s of %s" %(self.game.house_card[0].value,self.game.house_card[0].suit)
    #     tmp_player_card = "%s of %s" %(self.game.player_card[0].value, self.game.player_card[0].suit)

    #     self.assertEqual(self.game.deck.find(tmp_house_card),[])
    #     self.assertEqual(self.game.deck.find(tmp_player_card),[])
    #     self.assertEqual(self.game.deck.size,50)

    #     self.game.return_card()
    #     self.assertEqual(self.game.deck.size,52)
    #     self.assertNotEqual(self.game.deck.find(tmp_house_card),[])
    #     self.assertNotEqual(self.game.deck.find(tmp_player_card),[])

    #     self.game.deal_card()
    #     self.game.deal_card()
    #     self.assertEqual(self.game.deck.size,48)

    #     self.game.return_card()
    #     self.assertEqual(self.game.deck.size,52)

    @mock.patch("builtins.input")
    @mock.patch("builtins.print")
    def test_start_game(self,fake_print,fake_input):
        """
        Test start game
        """

        fake_input.side_effect = ["l", "c", "l",'c', "h", "c", "h", "c",'l']

        deal_side_effects =[
             # 1st match
            {"value":"8", "suit":"Spades"}, {"value":"2", "suit":"Hearts"},
            # 2nd match
           {"value":"Ace", "suit":"Clubs"}, {"value":"Ace", "suit":"Hearts"},
            # 3rd match
           {"value":"Ace", "suit":"Spades"},{"value":"Jack", "suit":"Hearts"},
            # 4th match
            {"value":"9", "suit":"Diamonds"}, {"value":"10", "suit":"Diamonds"},
            # 5th match
            {"value":"3", "suit":"Hearts"},{"value":"2", "suit":"Diamonds"},
        ]

        self.game.deck.deck_deal = mock.Mock(side_effect= deal_side_effects)
        self.assertRaises(StopIteration, self.game.start_game)

        # 1st c
        # 2nd w
        # 3rd  c
        # 4th c
        # 5th 75 -25 + 0 = 50 (lost)
        # stop before the 5th matcg 50 -25 = 25

        self.assertEqual(self.game.player_score,60)
        # self.assertEqual(self.game.player_score,10)

    # @mock.patch("builtins.input")
    # @mock.patch("builtins.print")
    # def test_lose(self, fake_print, fake_input):
    #     deal_side_effects = [
    #         # 1st match
    #         Stack(cards=[Card("3", "Spades")]), Stack(cards=[Card("2", "Hearts")]),
    #         # 2nd match
    #         Stack(cards=[Card("Queen", "Clubs")]), Stack(cards=[Card("King", "Hearts")]),
    #     ]
    #     fake_input.side_effect =['h','l']

    #     # game = CardGame(reward = 20, player_score = 60, cost =30)
    #     self.game.deck.deal = mock.Mock(side_effect = deal_side_effects)
    #     self.game.start_game()
        
    #     self.assertEqual(self.game.player_score,0)
    #     fake_print.assert_called_with("You lost with 0 points.")
    
    # @mock.patch("builtins.input")
    # @mock.patch("builtins.print")
    # def test_win(self, fake_print, fake_inputs):
    #     deal_side_effects =[
    #         # 1st match
    #         Stack(cards=[Card("3", "Spades")]), Stack(cards=[Card("Ace", "Hearts")]),
    #         # 2nd match
    #         Stack(cards=[Card("8", "Clubs")]), Stack(cards=[Card("King", "Hearts")]),
    #         # 3rd match
    #         Stack(cards=[Card("Ace", "Spades")]), Stack(cards=[Card("Queen", "Hearts")]),
    #         # 4th match
    #         Stack(cards=[Card("9", "Diamonds")]), Stack(cards=[Card("5", "Diamonds")]),
    #     ]

    #     fake_inputs.side_effect = ["l", "c", "h", "c", "h", "c", "l", "s"]
    #     #game = CardGame(reward = 20, player_score = 60, cost =30)
    #     self.game.deck.deal = mock.Mock(side_effect = deal_side_effects)
    #     self.game.player_score = 990
    #     self.game.start_game()

    #     self.assertEqual(self.game.player_score, 1120)
    #     fake_print.assert_called_with("Congratulations! You won with 1120 points!")
    
    # def test_error_suit(self):
    #     """
    #     Test raise exception for showing wrong suit
    #     """
    #     side_effects =[
    #         # 1st game
    #         Stack(cards=[Card("Ace", "NO SUIT")]),
    #         Stack(cards=[Card("Ace", "Hearts")])
    #     ]

    #     self.game.deck.deal = mock.Mock(side_effect = side_effects)
    #     self.game.deal_card()
    #     self.assertRaises(Exception, self.game.reveal_house_card)

    
    # @mock.patch("builtins.input")
    # @mock.patch("builtins.print")
    # def test_equal_stop(self, fake_print, fake_input):
    #     deal_side_effects =[
    #          # 1st match
    #         Stack(cards=[Card("3", "Spades")]), Stack(cards=[Card("King", "Hearts")]),
    #         # 2nd match
    #         Stack(cards=[Card("Queen", "Clubs")]), Stack(cards=[Card("Queen", "Hearts")]),
    #     ]

    #     fake_input.side_effect = ['h','c','l','s']

    #     self.game.deck.deal = mock.Mock(side_effect= deal_side_effects)
    #     self.assertRaises(StopIteration, self.game.start_game)

    #     #self.assertEqual(self.game.player_score, 40)
    #     self.assertEqual(self.game.player_score, 40)
    #     #60 -30 +20
    #     # 60 -30 + 20

if __name__ ==  "__main__":
    unittest.main()
