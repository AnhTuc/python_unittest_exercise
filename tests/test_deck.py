import unittest
from unittest import mock
from dev.deck import Deck

import random
class TestDeck(unittest.TestCase):
    def setUp(self) -> None:
        self.deck = Deck()

    def test_deal_card(self):
        """
        Test deal card from deck
        """
        with mock.patch.object(random,'randint') as fake_random:
            val = "8"
            suit ="Clubs"
            fake_random.side_effect =[5,2]
            card = Deck().deck_deal()
            self.assertEqual(card['value'], val)
            self.assertEqual(card['suit'], suit)

    def test_duplicate_card(self):
        """
        Test assign only unique cards
        """
        with mock.patch.object(random,'randint') as fake_random:
            fake_random.side_effect = [0,2,0,2,0,1]
            card1 = self.deck.deck_deal()
            card2 = self.deck.deck_deal()
            self.assertEqual(len(self.deck.give_away),2)

            values = list(Deck.CARD_RANK['values'].keys())
            suits = list(Deck.CARD_RANK['suits'].keys())
            v_i, s_i = self.deck.give_away.pop()
            tmp = {"value":values[v_i],"suit":suits[s_i]}

            self.assertEqual(tmp, card2)


    def test_return_card(self):
        """
        Test return card to deck
        """
        card1 = self.deck.deck_deal()
        card2 = self.deck.deck_deal()

        self.deck.return_card(1)
        self.assertEqual(len(self.deck.give_away),1)

        values = list(Deck.CARD_RANK['values'].keys())
        suits = list(Deck.CARD_RANK['suits'].keys())
        v_i, s_i = self.deck.give_away[0]
        tmp = {"value":values[v_i],"suit":suits[s_i]}

        self.assertEqual(tmp, card1)

if __name__ =="__main__":
    unittest.main()