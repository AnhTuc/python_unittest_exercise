import logging
import unittest
from unittest import mock

# import sys
# import os
# sys.path.append(os.getcwd())

from dev.card_game import CardGame
from dev.player import Player
from dev.deck import Deck
from dev.helper import *

class TestGameCard(unittest.TestCase):
    def setUp(self):
        self.player = Player(player_score = 60, name ='abc')
        self.game = CardGame(reward = 20, cost =30)

    def test_deal_card(self):
        """
        Test if host and player each has a card
        """
       
        #self.assertEqual(self.game.deck.size,52)
        self.assertIsNone(self.game.card)
        self.assertIsNone(self.player.card)
        # self.player.card = self.game.deal_card()
        # self.assertIsNotNone(self.game.card)
        # self.assertIsNotNone(self.player.card)

        side_effects = [
            {'value':"King",'suit':"Diamonds"}, 
            {'value': "8",'suit':"Hearts"}
        ]
        with mock.patch.object(Deck, 'deck_deal') as fake_deck:
            fake_deck.side_effect = side_effects
            self.player.card = self.game.deal_card()
            self.assertEqual(self.player.card,{'value': "8",'suit':"Hearts"})

    def test_card_info(self):
        """
        Test retrive card's info
        """
        side_effects = [
            {'value':"Ace",'suit':"Spades"}, {'value':"2",'suit':"Spades"},
            # 2nd game
            {'value':"King",'suit':"Diamonds"}, {'value': "8",'suit':"Hearts"}
        ]
        card = mock.Mock(side_effect=side_effects)
        self.assertEqual(Deck.get_card_info(card()),'A\u2660')
        self.assertEqual(Deck.get_card_info(card()),'2\u2660')
        self.assertEqual(Deck.get_card_info(card()),'K\u2666')
        self.assertEqual(Deck.get_card_info(card()),'8\u2665')

    @mock.patch("builtins.print")
    def test_reveal_card(self, fake_print):
        """
        Test if the house card is reveal correctly
        """
        self.game.deal_card()
       
        with mock.patch.dict(self.game.card,{'value':'Ace', 'suit':'Spades'}) as fake_card:
            self.game.reveal_card(fake_card)
            fake_print.assert_any_call("House has A\u2660")

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
        """
        Test player continue round or not
        """
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
    
    @mock.patch('builtins.input')
    def test_play_match(self, fake_input):
        """
        Test a play round
        """
        side_effects =[('lower','lower'),('higher','higher'),('lower','higher')]
        self.game.start_match = mock.Mock(side_effect=side_effects)

        fake_input.side_effect =['co','c','s','c']
        
        with mock.patch('builtins.print') as fake_print:
            self.game.play_match(self.player)
            # 60 +40 = 100 --> score only minus when starting the whole match
            self.game.play_match(self.player)
            self.assertEqual(self.player.score,100)

    @mock.patch("builtins.input")
    @mock.patch("builtins.print")
    def test_start_match(self, fake_print, fake_input):
        """
        Test round's begin by dealing cards and user guessing
        """
        side_effects = [
            {'value':"Ace",'suit':"Spades"}, {'value':"2",'suit':"Spades"},
            # 2nd game
            {'value':"King",'suit':"Spades"}, {'value': "8",'suit':"Hearts"},
        ]

        fake_input.side_effect = ['higher','lg','lower']

        with mock.patch.object(Deck, 'deck_deal') as fake_deck:
            fake_deck.side_effect = side_effects
            guess, result = self.game.start_match(self.player)
            self.assertEqual(guess,'higher')
            self.assertEqual(result,'higher')

            guess, result = self.game.start_match(self.player)
            self.assertEqual(guess,'lower')
            self.assertEqual(result,'lower')
     
    @mock.patch("builtins.input")
    @mock.patch("builtins.print")
    def test_start_game(self,fake_print,fake_input):
        """
        Test start game
        """

        fake_input.side_effect = ["l", "c", "l",'s', "h", "c", "h", "c",'l','s']

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

        with mock.patch.object(Deck, 'deck_deal') as fake_deck:
            fake_deck.side_effect = deal_side_effects
            self.assertRaises(StopIteration, self.game.start_game, self.player)
            #1st: win
            #2nd: win and stop --> 60 +40 -30 = 70
            #3rd: win
            #4rd: win
            #5th: win --> score minus before match --> 40, score minus after match: 70
            #if add stop into after 5th round--> 70 + 80 -30 =120
            self.assertEqual(self.player.score,120)
    
    @mock.patch("builtins.input")
    @mock.patch("builtins.print")
    def test_win(self, fake_print, fake_input):
        """
        Test player win game
        """
        fake_input.side_effect = ["l", "c", "h", "c", "h", "c", "l", "s"]

        deal_side_effects =[
             # 1st match
            {"value":"8", "suit":"Spades"}, {"value":"2", "suit":"Hearts"},
            # 2nd match
           {"value":"Ace", "suit":"Clubs"}, {"value":"King", "suit":"Hearts"},
           {"value":"Ace", "suit":"Spades"},{"value":"Jack", "suit":"Hearts"},
            {"value":"3", "suit":"Hearts"},{"value":"2", "suit":"Diamonds"}
        ]

        with mock.patch.object(Deck, 'deck_deal') as fake_deck:
            fake_deck.side_effect = deal_side_effects
            self.player.score = 990
            self.game.start_game(self.player)
            # 990 + 60 -30 +160 = 1180 -> old version when player.score += game.score
            #new version player got direct score : 990 -30 + 160 =1120
            self.assertEqual( self.player.score,1120)
            fake_print.assert_called_with("Congratulations! You won with 1120 points!" )
    

    @mock.patch("builtins.input")
    @mock.patch("builtins.print")
    def test_lose(self, fake_print, fake_input):
        """
        Test player lose game
        """
        fake_input.side_effect = ["l", "s", "h"]

        deal_side_effects =[
             # 1st match
            {"value":"8", "suit":"Spades"}, {"value":"2", "suit":"Hearts"},
            # 2nd match
           {"value":"Ace", "suit":"Clubs"}, {"value":"Ace", "suit":"Hearts"}
        ]

        with mock.patch.object(Deck, 'deck_deal') as fake_deck:
            fake_deck.side_effect = deal_side_effects
            self.game.start_game(self.player)
            self.assertEqual(self.player.score,20)
            fake_print.assert_called_with("You lost with 20 points.")

if __name__ == "__main__":
    unittest.main()
