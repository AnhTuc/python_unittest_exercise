import time
# import sys
# import os
# sys.path.append(os.getcwd())

# import dev.config as config
from . import config
from dev.helper import *
from dev.deck import Deck


class CardGame:
    
    def __init__(self, match = 1, reward = 20, cost = 25):
        self.reward = reward
        self.cost = cost
        self.card = None
        self.deck = Deck()
        self.match = match
      
    @property
    def card(self): 
        return self._card
    
    @card.setter
    def card(self,house_card):
        self._card = house_card

    def reveal_card(self,card,name='House'):
        """
        Show the house's card
        """
        card_info = Deck.get_card_info(card)
        print("%s has %s" % (name,card_info))
        Deck.draw_card(card)

    def deal_card(self):
        """
        Assign cards for host and player
        """
        self.card = self.deck.deck_deal()
        player_card = self.deck.deck_deal()

        # while(self.card == player_card):
        #     player_card = Deck.deck_deal()
        return player_card
    
    def return_card(self, player):
        """
        Reset round. Take cards back to deck
        """
        self.card = None
        player.card = None
        self.deck.return_card(2)
    
    def player_guess(self, possible_input):
        """
        Input guess value higher or lower
        """
        house_card_info = Deck.get_card_info(self.card)
        print("Is your card lower(l) or higher(h) than %s" %house_card_info)
        guess = process_input(input(), possible_input)

        while (guess != 'lower' and guess !="higher") :
            config.logger.warning("Invalid user's input")
            print("Invalid input %s, it has to be higher(h) or lower(l)" %guess)
            guess = process_input(input(), possible_input)
        
        return guess
    
    def compare_card(self, house_card, player_card, id ='value'):
        """
        Compare house's card and player's card
        """

        rank_house = Deck.CARD_RANK[id +'s'][house_card[id]]
        rank_player = Deck.CARD_RANK[id +'s'][player_card[id]]

        if rank_house > rank_player:
            return 'lower'
        elif rank_house < rank_player:
            return 'higher'
        else:
            try:
                return self.compare_card(house_card, player_card, id ='suit')
            except:
                print("Error deck deal the same card for player")
    
    def player_continue(self):
        """
        Continue or quit game
        """
        possible_inputs = ['continue', 'stop']
        print("Would you like to continue(c) or stop(s)?")
        s_or_c = process_input(input(),possible_inputs)

        while (s_or_c not in possible_inputs):
            config.logger.warning("Invalid user's input")
            print("Invalid input: %s, stop(s) or continue(c)" %s_or_c)

            s_or_c = process_input(input(),possible_inputs)
        
        return s_or_c
    

    def start_match(self, player):
        """
        Starting match by dealing card and getting user's guess
        """
        print("\nYour current score is: %d" % player.score)
        player.card = self.deal_card()
        self.reveal_card(self.card)

        guess = self.player_guess(['higher','lower'])
        result = self.compare_card(self.card, player.card)
        self.reveal_card(player.card,player.name)
        self.return_card(player)
        return guess, result
    
    def play_match(self,player):
        """
        Process sequence of correct answer within a match
        """
        if player.tmp_reward == 0:
            player.tmp_reward = self.reward
        player_continue = True

        while player_continue:
            guess, result = self.start_match(player)
            if guess == result:
                print("Your guess is correct!\nYou earned %d" %player.tmp_reward)
                player_continue =self.player_continue()

                if player_continue =='stop':
                    player.score += player.tmp_reward
                    player.tmp_reward = 0
                    break
                else:
                    player.tmp_reward *=2

            else:
                print("Your guess is incorrect!\nYou lose %d reward points\n"%player.tmp_reward)
                time.sleep(2)
                player.tmp_reward = 0
                break
    
    
    def introduction(func):
        """
        Game introduction cost and reward
        """
        def inner(self,*args, **kwargs):
            print("Welcome %s to card game! I am be your host of today!" %(args[0].name))
            print("Game Start!")
            time.sleep(1)
            print("You have %d points" %(args[0].score))
            time.sleep(1)
            print("Cost for playing is %d points" % self.cost)
            time.sleep(1)
            print("Initial reward is %d points" % self.reward)
            time.sleep(1)
            func(self,*args, **kwargs)
        return inner
    
    @introduction   
    def start_game(self, player):
        """
        Guessing game
        """  
        # self.introduction()
        game_over = False
        while not game_over:
            print("Your current in match: %d\n" %self.match)
            time.sleep(1)
            self.play_match(player)
            player.score -= self.cost
            self.match += 1
            game_over = check_game_over(player.score)




        