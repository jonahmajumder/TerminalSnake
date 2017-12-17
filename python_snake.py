# python_snake.py

from terminaltools import *
import time, datetime

from blessings import Terminal
from getch import getch, getche
import unichars as ch
from make_snake import start_snake

t = Terminal()

BRDR_CLR = 9
WHITE = 256
BLK = 0

settings = [(True, ['Start Speed','5','10','15','30'], (1, 1)), (True, ['Start Length','5','10','15','20'], (1, 1)), (False, ['GO BACK', 'PLAY'], (3, 4))]

sp = TitleScreen(
    'SNAKE',
    settings,
    border_color=BRDR_CLR,
    title_color=BLK,
    background_color=WHITE,
    secondary_color=27,
    button_color=250,
    stale_color=4,
)
sp.start()
start_length = int(sp.settings['Start Length'])
start_speed = int(sp.settings['Start Speed'])

start_snake(t, start_speed, start_length,
    snake_color=BLK,
    food_color=9,
    border_color=BRDR_CLR,
    background_color=WHITE,
)