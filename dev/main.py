from dev.player import Player
from dev.helper import *
from dev.card_game import CardGame
import time
import logging

# @handle_exception
def game_continue(house = CardGame(), player = Player(name ='')):
    if not check_game_over(player.score):
        s_or_c = process_input(input("Do you want to to close game? (stop(s) to stop game)."),['stop'])
        if s_or_c == 'stop':
            try:
                print("Closing card game...")
                sys.exit(1)
            except SystemExit:
                os._exit(1)
            #sys.exit(1)
        else:
            print("Retrieve game ...\n"+"."*20)
            time.sleep(1)
            match_config = dict(match_cont = house.match, player_name = player.name, start_score = player.score, tmp_rw = player.tmp_reward)
            card_game(**match_config)

def card_game(match_cont = 1, player_name = None, start_score = 60, rw = 50, tmp_rw = 0):
    try:
        player1 = Player(name = player_name, receive_reward= tmp_rw, player_score = start_score)
        game = CardGame(match = match_cont, reward = rw)
        game.start_game(player1)

    except (KeyboardInterrupt):
            logging.warning("\nKeyboard Interrupt: Closing Card game?")
            game_continue(house = game, player = player1)
    except BaseException:
        logging.warning("\nError Approach. Closing Card game.")


if __name__ == "__main__":
    card_game()