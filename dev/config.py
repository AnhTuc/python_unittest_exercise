import logging
from logging import FileHandler, Formatter

# import sys
# import os
# sys.path.append(os.getcwd())

logger = logging.getLogger('card_game_log')
logger.setLevel(logging.DEBUG)
formater = Formatter('%(asctime)s - %(levelname)s - [in %(pathname)s : %(lineno)d] - %(message)s')

handler = FileHandler('log_card_game.log')
handler.setLevel(logging.INFO)
handler.setFormatter(formater)
logger.addHandler(handler)