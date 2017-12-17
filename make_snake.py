# roller

import sys, unichars
from blessings import Terminal
import numpy as np
from threading import Thread
from queue import Queue
from terminaltools import make_border
from blockletters import make_letter
from numpy.random import random_integers
from time import sleep
from polling import Keypoller
from getch import getch, getche

t = Terminal()

def start_snake(terminal, pixels_per_second, length, snake_color=0, food_color=9, border_color=0, background_color=256):
    border_top = 2
    1. / pixels_per_second

    def change_loc(loc, side):
        new_loc = [(loc[0]+1, loc[1]), (loc[0], loc[1]+1), (loc[0]-1, loc[1]), (loc[0], loc[1]-1)]
        return new_loc[side]

    def new_food(terminal, body_locs, edge_x, edge_y):
        valid = False
        while not valid:
            food_loc = (random_integers(edge_y[0] + 1, edge_y[1] - 1), random_integers(random_integers(edge_x[0] + 1, edge_x[1] - 1)))
            valid = food_loc not in body_locs
        return food_loc

    def print_score(terminal, score):
        score_str = 'Score: ' + str(score)
        score_print_str = terminal.move(0, terminal.width - len(score_str) - 2)
        score_print_str += terminal.bold + terminal.color(border_color) + score_str + terminal.normal
        print score_print_str

    def disp_message(terminal, message, y_offset=0):
        width = terminal.width
        height = terminal.height - 2
        mid_loc = ((height - height%2)/2, (width - width%2)/2)
        x_offset = (len(message) - len(message)%2)/2
        print_str = terminal.move(mid_loc[0] + y_offset, mid_loc[1] - x_offset)
        print_str += terminal.normal + terminal.bold + message
        print_str += terminal.move(height, 0) + terminal.normal
        print print_str

    def quit_game(terminal, message, score, speed, length):
        disp_message(terminal, message, y_offset=-2)
        score_str = 'Score: ' + str(score)
        speed_str = 'Final Speed: ' + str(speed) + ' pixels per second'
        len_str = 'Final Length: ' + str(length) + ' pixels' 
        for i, s in enumerate([score_str, speed_str, len_str]):
            disp_message(terminal, s, y_offset=i)
        sys.exit()

    width = terminal.width - 1
    height = terminal.height - 2
    mid_loc = ((height - height%2)/2, (width - width%2)/2)
    print terminal.on_color(background_color) + make_border(terminal, border_color, top=border_top) + terminal.normal

    edge_x = [0, width]
    edge_y = [border_top, height]

    rand_x = random_integers(edge_x[0] + 1, edge_x[1] - 1)
    rand_y = random_integers(edge_y[0] + 1, edge_y[1] - 1)
    pos = [(edge_y[0], rand_x), (rand_y, edge_x[0]), (edge_y[1], rand_x), (rand_y, edge_x[1])]
    side = random_integers(0, 3)
    entry = pos[side]

    body_locs = [entry]
    brdr_char = [unichars.HOR, unichars.VERT, unichars.HOR, unichars.VERT][side]

    brdr_char = terminal.on_color(background_color) + terminal.color(border_color) + brdr_char + terminal.normal

    side_char = {'s':0, 'd':1, 'w':2, 'a':3}

    score = 0
    print_score(terminal, score)

    disp_message(terminal, 'Get ready!')
    sleep(.5)
    disp_message(terminal, '            ')
    sleep(.5)
    num_loc = (mid_loc[1]-2, mid_loc[0]-3)
    for num in ['3', '2', '1']:
        print make_letter(terminal, num, num_loc, 0)
        sleep(.5)
        print make_letter(terminal, 'CLEAR', num_loc, 0)
        sleep(.5)

    with Keypoller() as poller:
        print terminal.move(*body_locs[0]) + terminal.on_color(snake_color) + ' ' + terminal.move(height, 0) + terminal.normal
        food_loc = new_food(terminal, body_locs, edge_x, edge_y)
        print terminal.on_color(food_color) + terminal.move(*food_loc) + ' ' + terminal.normal + terminal.move(height, 0)
        try:
            while True:
                if side in [1,3]:
                    sleep((1. / pixels_per_second)) # wait
                elif side in [0,2]:
                    sleep((1. / pixels_per_second)*1.5)
                key = poller.poll()
                if (key in ['a', 's', 'd', 'w']):
                    if abs(side - side_char[key]) != 2:
                        side = side_char[key]
                new_loc = change_loc(body_locs[-1], side)
                inScreen = not ((new_loc[0] in edge_y) or (new_loc[1] in edge_x)) # check if newest (last) is in the screen
                hit_self = new_loc in body_locs
                body_locs.append(new_loc) # add new to list as newest (last)
                body_length = len(body_locs)
                if not inScreen:
                    lose_msg = 'You hit the edge, you lose!'
                    quit_game(terminal, lose_msg, score, pixels_per_second, length)
                elif hit_self:
                    lose_msg = 'You collided with yourself, you lose!'
                    quit_game(terminal, lose_msg, score, pixels_per_second, length)
                else:
                    if food_loc in body_locs:
                        food_loc = new_food(terminal, body_locs, edge_x, edge_y)
                        print terminal.on_color(food_color) + terminal.move(*food_loc) + ' ' + terminal.normal + terminal.move(height, 0)
                        score += pixels_per_second
                        print_score(terminal, score)
                        pixels_per_second += 1
                        length += 2
                    print terminal.move(*body_locs[-1]) + terminal.on_color(snake_color) + ' ' + terminal.normal + terminal.move(height, 0) # print newest (last) to screen if in screen
                    if body_length > length:
                        print terminal.move(*body_locs[0]) + terminal.normal + brdr_char + terminal.move(height, 0)
                        brdr_char = terminal.on_color(background_color) + ' ' + terminal.normal
                        body_locs = body_locs[-length:]
        except KeyboardInterrupt:
            lose_msg = 'You pressed Ctrl-C to quit mid-game!'
            quit_game(terminal, lose_msg, score, pixels_per_second, length)





