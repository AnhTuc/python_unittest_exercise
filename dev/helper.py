import random
import os
import sys
import logging

def process_input(user_input, possible_inputs):
    """
    Format player input
    """
    answer = iter(possible_inputs)
    for pos in answer:
        if user_input.lower() == pos  or user_input.lower() == pos[0]:
            return pos
    return user_input


WIN_POINT = 1000
LOSE_POINT = 30
def check_game_over(player_score):
    """
    Check enough to play another match
    """
    if player_score >= WIN_POINT:
        print("Congratulations! You won with %s points!" % player_score)
        return True
    elif player_score < LOSE_POINT:
        print("You lost with %s points." % player_score)
        return True
    else:
        return False


def handle_exception(func):
    """
    Handle upcoming exception while the game is playing
    Problem when accident stop --> need to ask back
    """
    def inner(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except (KeyboardInterrupt):
            logging.warning("Keyboard Interrupt: Closing Card game?")

        except BaseException as b:
            logging.warning("Error Approach. Closing Card game?")
    
        finally:
            try:
                    sys.exit()
            except SystemExit:
                    os._exit(1)
    return inner


