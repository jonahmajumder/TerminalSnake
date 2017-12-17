# Keypoller
# Jonah Majumder
# from http://stackoverflow.com/questions/13207678/whats-the-simplest-way-of-detecting-keyboard-input-in-python-from-the-terminal
# 7/20/16

import sys
import select
import termios
import time


class Keypoller(object):
    def __enter__(self): 
        self.fd = sys.stdin.fileno()
        self.new_term = termios.tcgetattr(self.fd)
        self.old_term = termios.tcgetattr(self.fd)

        self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)

        return self

    def __exit__(self, type, value, traceback):
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)

    def poll(self):
        dr,dw,de = select.select([sys.stdin], [], [], 0)
        if not dr == []:
            return sys.stdin.read(1)
        return None

# ----------- Usage Example -----------------

# with Keypoller() as keypoller:
#     polls = 0
#     while True:
#         char = keypoller.poll()
#         polls += 1
#         if not (char is None):
#             print char
#             print polls
#             break

