# terminaltools.py
# Jonah Majumder
# 7/15/16

from blessings import Terminal
from polling import Keypoller
import time, datetime, sys, os
import unichars
import blockletters
from threading import Thread
from queue import Queue
from getch import getch, getche

def make_odd(n):
    n_odd = n
    if n % 2 == 0:
        n_odd -= 1
    else:
        pass
    return n_odd

def reset_cursor(terminal):
    return terminal.move(terminal.height - 2, 0)

def make_border(terminal, color, top=1, specify_size=0, newsize=[60,20]):
    if specify_size:
        border_width = newsize[0]
        border_height = newsize[1]
    else:
        border_width = make_odd(terminal.width)    
        border_height = terminal.height
    clear_line = terminal.move(0,0)
    for i in range(terminal.width):
        clear_line += ' '
    print clear_line
    border = terminal.color(color)
    for iRow in range(1, border_height - 1):
        with terminal.location(0, iRow):
            if iRow < top:
                startChar = ' '
                midChar = ' '
                endChar = ' '
            elif iRow == top:
                startChar = unichars.UL_CORNER
                midChar = unichars.HOR
                endChar = unichars.UR_CORNER
            elif iRow == border_height - 2:
                startChar = unichars.LL_CORNER
                midChar = unichars.HOR
                endChar = unichars.LR_CORNER
            else:
                startChar = unichars.VERT
                midChar = ' '
                endChar = unichars.VERT
            border += startChar
            for iCol in range(border_width - 2):
                border += midChar
            border += endChar + '\n'
    border = border[:-1] + terminal.normal
    return border

def info_screen(terminal, color):
    print_string = ''
    return print_string

def coerce_value(n, n_max, n_min=0):
    if not n_max > n_min:
        print 'Max value must be larger than min value.'
        return -1
    else:
        if n > n_max:
            return n_max
        elif n < n_min:
            return n_min
        else:
            return n

def splash_coordinates(terminal, x_splash, y_splash):
    min_x = 0
    max_x = make_odd(terminal.width) - 2
    splash_width = max_x - min_x
    min_y = 2
    max_y = terminal.height - 3
    splash_height = max_y - min_y
    if (x_splash in range(0, splash_width)) and (y_splash in range(0, splash_height)):
        x_true = x_splash + min_x
        y_true = y_splash + min_y
        return (x_true, y_true)
    else:
        raise Exception('Out of range on splash screen!')

def make_clearer_string(terminal):
    x1, y1 = splash_coordinates(terminal,0,0)
    x0 = x1 - 1
    y0 = y1 - 1
    clearStr = '' 
    clearStr += terminal.move_x(x0) + terminal.move_y(y0) + terminal.clear_eol
    for line in range(terminal.height - 3):
        clearStr += terminal.move_down
        clearStr += terminal.clear_eol
    return clearStr

def rect_string(terminal, strt, width, height, color, fill=False):
    s = ''
    locs = [[],[]]
    for icol in range(width):
        locs[0].append(icol)
        locs[1].append(0)
    for irow in range(1, height - 1):
        locs[0].append(0)
        locs[1].append(irow)
        locs[0].append(1)
        locs[1].append(irow)
        if fill:
            for icol in range(2, width - 2):
                locs[0].append(icol)
                locs[1].append(irow)
        locs[0].append(width - 2)
        locs[1].append(irow)
        locs[0].append(width - 1)
        locs[1].append(irow)
    for icol in range(width):
        locs[0].append(icol)
        locs[1].append(height - 1)

    for blk in range(len(locs[0])):
        s += terminal.move_x(strt[0] + locs[0][blk])
        s += terminal.move_y(strt[1] + locs[1][blk])
        s += terminal.on_color(color) + ' ' + terminal.normal

    s += terminal.move(terminal.height - 2, 0)
    return s

# def animate_rect(string_tuple, in_q):
#     rate = .1
#     s1, s2 = string_tuple
#     stop_signal = False
#     ctr = 0
#     while not stop_signal:
#         while True:
#             ctr += 1
#             stop_signal = in_q.get()
#             print s1
#             time.sleep(rate)
#             print s2
#             time.sleep(rate)
#             # if ctr > 50:
#             #     break

# def button_changer(out_q):
#     stop_signal = False
#     ctr = 0
#     while not stop_signal:
#         ctr += 1
#         char = raw_input()
#         if char == 's':
#             stop_signal = True
#         else:
#             stop_signal = False
#         out_q.put(stop_signal)
#         # if ctr > 50:
#         #     break


class TitleScreen(object):
    def __init__(self, name, settings_options, border_color=4, title_color=9, background_color=231, secondary_color=40, button_color=12, stale_color=22):
        self.t = Terminal()
        self.title = name
        self.settings_options = settings_options
        self.settings_active_buttons = [option[0] for option in self.settings_options]
        self.border_color = border_color
        self.title_color = title_color
        self.background_color = background_color
        self.secondary_color = secondary_color
        self.button_color = button_color
        self.stale_color = stale_color
        self.title_button_labels = ['PLAY', 'RULES', 'QUIT']
        self.width = make_odd(self.t.width)
        self.middle_x = (self.width - 1)/2
        self.height = self.t.height - 4
        with open("rules.txt", "r") as myfile:
            self.rulesMsg = myfile.readlines()

        self.border = self.t.on_color(self.background_color) + make_border(self.t, self.border_color) + self.t.normal
        letter_xs = []
        if len(self.title) % 2 == 0:
            for (iletter, letter) in enumerate(self.title):
                x_offset = iletter - len(self.title)/2
                letter_xs.append((self.middle_x + (x_offset*(blockletters.LETTER_WIDTH + 1) + 1),letter))
        else:
            for (iletter, letter) in enumerate(self.title):
                x_offset = iletter - (len(self.title) - 1)/2
                letter_xs.append((self.middle_x + (x_offset*(blockletters.LETTER_WIDTH + 1) - 2), letter))

        self.title_y = 2
        title_cursor_seq = ''
        for letter_tuple in letter_xs:
            letter_x = letter_tuple[0]
            letter = letter_tuple[1]
            true_coors = splash_coordinates(self.t, letter_x, self.title_y)
            letter_str = blockletters.make_letter(self.t, letter, true_coors, self.title_color)
            title_cursor_seq += letter_str
        title_cursor_seq += self.t.normal
        self.title_seq = title_cursor_seq
        print self.border
        print self.title_seq

    def make_buttons(self, labels, button_y, rowlabel=False, button_height=3, button_side_pad=4):
        label_y_relative = (button_height + (button_height % 2)) / 2 - 1
        button_label_y = splash_coordinates(self.t, 0, button_y + label_y_relative)[1]
        button_separation=6

        button_label_lengths = [len(label) for label in labels]
        button_widths = [button_label_len + 2*button_side_pad for button_label_len in button_label_lengths]
        button_total_width = sum(button_widths) + (len(labels) - 1)*button_separation
        button_left_x = self.middle_x - ((button_total_width - (button_total_width % 2))/2)

        button_label_start_xs = []
        button_label_start_xs.append(button_left_x + button_side_pad)
        for i in range(1, len(labels)):
            new_x = button_label_start_xs[i-1] + button_label_lengths[i-1] + 2*button_side_pad + button_separation
            button_label_start_xs.append(new_x)
        button_x_locs = [loc - button_side_pad for loc in button_label_start_xs]
        n_buttons = len(button_x_locs)
        if rowlabel:
            n_buttons -= 1
            button_cursor_seq = self.t.on_color(self.background_color) + self.t.color(self.button_color)
            button_cursor_seq += self.t.bold
            button_cursor_seq += self.t.move_x(button_label_start_xs[0] - 1) + self.t.move_y(button_label_y)
            button_cursor_seq += labels[0] + ':' + self.t.normal
        else:
            button_cursor_seq = ''
        for i in range(len(labels) - n_buttons, len(labels)):
            button_coors = splash_coordinates(self.t, button_x_locs[i], button_y)
            button_cursor_seq += rect_string(self.t, button_coors, button_widths[i], button_height, self.button_color, fill=True)

        button_cursor_seq += self.t.on_color(self.button_color) + self.t.color(self.secondary_color)
        for i in range(len(labels) - n_buttons, len(labels)):
            button_cursor_seq += self.t.move_x(button_label_start_xs[i])
            button_cursor_seq += self.t.move_y(button_label_y)
            button_cursor_seq += labels[i]
        button_cursor_seq += self.t.normal + self.t.move(self.t.height - 2, 0)

        buttons = button_cursor_seq

        blinker_y = button_y - 1
        blinker_x_locs = [x - 2 for x in button_x_locs]
        blinker_widths = [width + 4 for width in button_widths]
        blinker_height = button_height + 2
        blinker_strings = []
        stale_blinker_strings = []
        blinker_ender_strings = []
        for i in range(len(labels) - n_buttons, len(labels)):
            blinker_coords = splash_coordinates(self.t, blinker_x_locs[i], blinker_y)
            blinker_str = rect_string(self.t, blinker_coords, blinker_widths[i], blinker_height, self.secondary_color, fill=False)
            stale_blinker_str = rect_string(self.t, blinker_coords, blinker_widths[i], blinker_height, self.stale_color, fill=False)
            blinker_ender_str = rect_string(self.t, blinker_coords, blinker_widths[i], blinker_height, self.background_color, fill=False)
            blinker_strings.append(blinker_str)
            stale_blinker_strings.append(stale_blinker_str)
            blinker_ender_strings.append(blinker_ender_str)

        blinkers = blinker_strings
        stale_blinkers = stale_blinker_strings
        blinker_enders = blinker_ender_strings

        return buttons, blinkers, stale_blinkers, blinker_enders

    def update_datetime(self):
        datetime_padding = 5

        hr = datetime.datetime.fromtimestamp(time.time()).strftime('%I')
        minute = datetime.datetime.fromtimestamp(time.time()).strftime(':%M %p')
        self.timestr = hr.lstrip('0') + minute
        time_cursor_seq = ''
        x_time, y_time = splash_coordinates(self.t, datetime_padding, self.height - 2)
        time_cursor_seq += self.t.move_x(x_time) + self.t.move_y(y_time)
        time_cursor_seq += self.t.on_color(self.background_color) + self.t.color(self.secondary_color)
        time_cursor_seq += self.t.bold + self.timestr + self.t.normal
        self.time = time_cursor_seq

        weekday = datetime.datetime.fromtimestamp(time.time()).strftime('%A, %B ')
        daynum = datetime.datetime.fromtimestamp(time.time()).strftime('%d, %Y')
        self.datestr = weekday + daynum.lstrip('0')
        date_cursor_seq = ''
        x_date, y_date = splash_coordinates(self.t, self.width - len(self.datestr) - datetime_padding, self.height - 2)
        date_cursor_seq += self.t.move_x(x_date) + self.t.move_y(y_date)
        date_cursor_seq += self.t.on_color(self.background_color) + self.t.color(self.secondary_color)
        date_cursor_seq += self.t.bold + self.datestr + self.t.normal
        self.date = date_cursor_seq

        print self.date
        print self.time

    def print_copyright(self):
        cr_msg = 'Made by Jonah Majumder on July 28, 2016.'
        len_cr = len(cr_msg)
        x_null, y_cr = splash_coordinates(self.t, 0, self.height - 10)
        x_cr = self.middle_x - (len_cr - (len_cr%2))/2
        cr_cursor_seq = self.t.move_y(y_cr) + self.t.move_x(x_cr)
        cr_cursor_seq += self.t.on_color(self.background_color) + self.t.color(self.secondary_color)
        cr_cursor_seq += self.t.bold + cr_msg + self.t.normal
        print cr_cursor_seq


    def do_buttons(self, button_labels, button_y, functions, start_cols, rowlabels, button_height, button_side_pad):
        rows = len(button_labels)
        buttons = ''
        blinkers = []
        stale_blinkers = []
        blinker_enders = []
        active_cols = []
        for i in range(rows):
            button_row, blinker_row, stale_blinker_row, blinker_ender_row = self.make_buttons(button_labels[i], button_y[i], rowlabels[i], button_height[i],  button_side_pad[i])
            buttons += button_row
            blinkers.append(blinker_row)
            stale_blinkers.append(stale_blinker_row)
            blinker_enders.append(blinker_ender_row)
            active_cols.append(start_cols[i])

        print buttons
        active_row = rows - 1
        for irow in range(rows):
            if irow == active_row:
                print blinkers[irow][active_cols[irow]]
            else:
                print stale_blinkers[irow][active_cols[irow]]

        print self.t.move(self.t.height - 2, 0)
        try:
            while True:
                char = getch()
                if char == 'w':
                    if active_row > 0:
                        print stale_blinkers[active_row][active_cols[active_row]]
                        print blinkers[active_row - 1][active_cols[active_row - 1]]
                        print self.t.move(self.t.height - 2, 0)
                        active_row -= 1
                elif char == 's':
                    if active_row < rows - 1:
                        print stale_blinkers[active_row][active_cols[active_row]]
                        print blinkers[active_row + 1][active_cols[active_row + 1]]
                        print self.t.move(self.t.height - 2, 0)
                        active_row += 1
                elif char == 'a':
                    if active_cols[active_row] > 0:
                        print blinker_enders[active_row][active_cols[active_row]]
                        print blinkers[active_row][active_cols[active_row] - 1]
                        print self.t.move(self.t.height - 2, 0)
                        active_cols[active_row] -= 1
                elif char == 'd':
                    if active_cols[active_row] < len(blinkers[active_row]) - 1:
                        print blinker_enders[active_row][active_cols[active_row]]
                        print blinkers[active_row][active_cols[active_row] + 1]
                        print self.t.move(self.t.height - 2, 0)
                        active_cols[active_row] += 1
                elif char == u'\n':
                    if active_row == rows - 1:
                        break
                    else:
                        print stale_blinkers[active_row][active_cols[active_row]]
                        print blinkers[active_row + 1][active_cols[active_row + 1]]
                        print self.t.move(self.t.height - 2, 0)
                        active_row += 1
                else:
                    pass
        except KeyboardInterrupt:
            self.clean_exit()
        functions(active_cols)

    def title_function(self, active_cols):
        title_fns = [self.advance_to_settings, self.rules, self.clean_exit]
        title_fns[active_cols[len(active_cols)-1]]()

    def do_title_buttons(self, start_button):
        title_rowlabel = False
        start_button -= title_rowlabel
        self.do_buttons([self.title_button_labels], [self.title_y + 9], self.title_function, [start_button], [title_rowlabel], [3], [4])

    def do_settings_buttons(self, settings_options):
        settings_button_labels = []
        y_locs = []
        rowlabels = []
        start_buttons = []
        button_heights = []
        button_paddings = []

        for s in range(len(settings_options)):
            option = settings_options[s]
            rowlabels.append(option[0])
            y_locs.append(2 if s == 0 else y_locs[s-1] + button_heights[s-1] + 3)
            settings_button_labels.append(option[1])
            button_heights.append(option[2][0])
            button_paddings.append(option[2][1])

        self.do_buttons(settings_button_labels, y_locs, self.process_settings, self.settings_active_buttons, rowlabels, button_heights, button_paddings)

    def process_settings(self, active_cols):
        self.settings_active_buttons = active_cols
        action_index = active_cols[len(active_cols) - 1]
        if action_index == 0:
            self.back_to_title('PLAY')
        elif action_index == 1:
            settings_dict = {}
            for iSetting, setting in enumerate(self.settings_options):
                if setting[0]:
                    settings_dict[setting[1][0]] = setting[1][setting[0] + active_cols[iSetting]]
            self.settings = settings_dict
            self.advance_to_game()
        else:
            raise Exception('Setting screen action index was not 0 or 1! How did that happen?!')

    def show_content(self):
        print self.title_seq
        self.update_datetime()
        self.print_copyright()


    def advance_to_settings(self):
        self.redraw_border()
        self.do_settings_buttons(self.settings_options)

    def advance_to_game(self):
        # self.redraw_border()
        # msg = str(self.settings)
        # with self.t.location(self.middle_x - ((len(msg) - (len(msg)%2))/2), 8):
        #     print self.t.bold + msg + self.t.normal
        # while True:
        #     char = getch()
        #     if char == u'\n':
        #         break
        pass

    def redraw_border(self):
        with self.t.location():
            print make_clearer_string(self.t)
        with self.t.location(0, 1):
            print self.border

    def back_to_title(self, title_button):
        self.redraw_border()
        self.show_content()
        self.do_title_buttons(self.title_button_labels.index(title_button))

    def rules(self):
        self.redraw_border()
        rulemsg = self.rulesMsg;
        for (iLine, line) in enumerate(rulemsg):
            with self.t.location(self.middle_x - ((len(line) - (len(line)%2))/2), 4 + iLine):
                print self.t.bold + line + self.t.normal
        while True:
            char = getch()
            if char == u'\n':
                break
        self.back_to_title('RULES')

    def clean_exit(self):
        with self.t.location():
            print make_clearer_string(self.t)
        msg = 'Thanks for playing ' + self.title + '!'
        with self.t.location(self.middle_x - ((len(msg) - (len(msg)%2))/2), 8):
            print self.t.bold + msg + self.t.normal
        sys.exit()

    def start(self):
        self.update_datetime()
        self.print_copyright()
        self.do_title_buttons(self.title_button_labels.index('PLAY'))


        




        


