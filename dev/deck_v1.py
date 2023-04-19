import random

class Deck:
    CARD_RANK={
        "values": {
            "King": 13,
            "Queen": 12,
            "Jack": 11,
            "10": 10,
            "9": 9,
            "8": 8,
            "7": 7,
            "6": 6,
            "5": 5,
            "4": 4,
            "3": 3,
            "2": 2,
            "Ace": 1,
        },
        "suits": {
            "Spades": 4,
            "Hearts": 1,
            "Clubs": 3,
            "Diamonds": 2
        }
    }

    SUIT_MAX = 3
    VALUE_MAX = 12

    def deck_deal():
        """
        Assign cards to house and player
        """
        values = list(Deck.CARD_RANK['values'].keys())
        suits =list(Deck.CARD_RANK['suits'].keys())

        value_house  = values[random.randint(0,Deck.VALUE_MAX)]
        suit_house = suits[random.randint(0,Deck.SUIT_MAX)]
        return {"value":value_house, "suit":suit_house}
    
    
    def get_card_symbol(card):
        """
        Get value of a card to symbol
        """
        if card['suit'] == "Spades":
            return "\u2660"
        elif card['suit'] == "Hearts":
            return "\u2665"
        elif card['suit'] == "Clubs":
            return "\u2663"
        elif card['suit'] == "Diamonds":
            return "\u2666"
    
    
    def get_card_value(card):
        """
        Get value of a card
        """
        if card['value'] == "Ace":
            return "A"
        elif card['value'] == "King":
            return "K"
        elif card['value'] == "Queen":
            return "Q"
        elif card['value']== "Jack":
            return "J"
        else:
            return card['value']
    
    def get_card_info(card):
        """
        Get information of card
        """
        card_value = Deck.get_card_value(card)
        card_suit = Deck.get_card_symbol(card)

        return "%s%s" % (card_value, card_suit)

    def draw_card(card):
        """
        Draw card using ascii
        """
        card_value = Deck.get_card_value(card)
        card_suit =Deck.get_card_symbol(card)
        card = (
            '┌─────────┐\n'
            '│{0}       │\n'
            '│         │\n'
            '│         │\n'
            '│    {1}   │\n'
            '│         │\n'
            '│         │\n'
            '│       {0}│\n'
            '└─────────┘\n'
        ).format(
            format(card_value, ' <2'),
            format(card_suit, ' <2'),
        )
        print(card.format(card_value,card_suit))
    
    