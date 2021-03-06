# blockletters
# Jonah Majumder
# 7/16/16

LETTER_WIDTH = 5
LETTER_HEIGHT = 6

def make_letter(terminal, letter, strt, color):
    from blessings import Terminal
    t = Terminal()
    if letter != 'CLEAR':
        letter = letter[0].upper()
        clr_char = False
    else: 
        clr_char = True

    locs = {
        'A': ([2,1,3,0,4,0,1,2,3,4,0,4,0,4],[0,1,1,2,2,3,3,3,3,3,4,4,5,5]),
        'B': ([0,1,2,3,0,4,0,1,2,3,0,4,0,4,0,1,2,3],[0,0,0,0,1,1,2,2,2,2,3,3,4,4,5,5,5,5]),
        'C': ([1,2,3,0,4,0,0,0,4,1,2,3],[0,0,0,1,1,2,3,4,4,5,5,5]),
        'D': ([0,1,2,0,3,0,4,0,4,0,3,0,1,2],[0,0,0,1,1,2,2,3,3,4,4,5,5,5,5]),
        'E': ([0,1,2,3,4,0,0,1,2,3,0,0,0,1,2,3,4],[0,0,0,0,0,1,2,2,2,2,3,4,5,5,5,5,5]),
        'F': ([0,1,2,3,4,0,0,1,2,3,0,0,0],[0,0,0,0,0,1,2,2,2,2,3,4,5]),
        'G': ([1,2,3,0,4,0,0,3,4,0,4,1,2,3],[0,0,0,1,1,2,3,3,3,4,4,5,5,5]),
        'H': ([0,4,0,4,0,1,2,3,4,0,4,0,4,0,4],[0,0,1,1,2,2,2,2,2,3,3,4,4,5,5]),
        'I': ([0,1,2,3,4,2,2,2,2,0,1,2,3,4],[0,0,0,0,0,1,2,3,4,5,5,5,5,5]),
        'J': ([0,1,2,3,4,2,2,0,2,0,2,0,1,2],[0,0,0,0,0,1,2,3,3,4,4,5,5,5]),
        'K': ([0,4,0,3,0,1,2,0,3,0,4,0,4],[0,0,1,1,2,2,2,3,3,4,4,5,5]),
        'L': ([0,0,0,0,0,0,1,2,3,4],[0,1,2,3,4,5,5,5,5,5]),
        'M': ([0,4,0,1,3,4,0,2,4,0,4,0,4,0,4],[0,0,1,1,1,1,2,2,2,3,3,4,4,5,5]),
        'N': ([0,4,0,1,4,0,2,4,0,3,4,0,4,0,4],[0,0,1,1,1,2,2,2,3,3,3,4,4,5,5]),
        'O': ([1,2,3,0,4,0,4,0,4,0,4,1,2,3],[0,0,0,1,1,2,2,3,3,4,4,5,5,5]),
        'P': ([0,1,2,3,0,4,0,4,0,1,2,3,0,0],[0,0,0,0,1,1,2,2,3,3,3,3,4,5]),
        'Q': ([1,2,3,0,4,0,4,0,4,0,3,1,2,4],[0,0,0,1,1,2,2,3,3,4,4,5,5,5]),
        'R': ([0,1,2,3,0,4,0,3,0,1,2,0,3,0,4],[0,0,0,0,1,1,2,2,3,3,3,4,4,5,5]),
        'S': ([1,2,3,4,0,1,2,3,4,4,0,1,2,3],[0,0,0,0,1,2,2,2,3,4,5,5,5,5]),
        'T': ([0,1,2,3,4,2,2,2,2,2],[0,0,0,0,0,1,2,3,4,5]),
        'U': ([0,4,0,4,0,4,0,4,0,4,1,2,3],[0,0,1,1,2,2,3,3,4,4,5,5,5]),
        'V': ([0,4,0,4,0,4,1,3,1,3,2],[0,0,1,1,2,2,3,3,4,4,5]),
        'W': ([0,4,0,4,0,4,0,2,4,0,2,4,1,3],[0,0,1,1,2,2,3,3,3,4,4,4,5,5]),
        'X': ([0,4,1,3,2,2,1,3,0,4],[0,0,1,1,2,3,4,4,5,5]),
        'Y': ([0,4,0,4,1,3,2,2,2],[0,0,1,1,2,2,3,4,5]),
        'Z': ([0,1,2,3,4,4,3,2,1,0,1,2,3,4],[0,0,0,0,0,1,2,3,4,5,5,5,5,5]),
        ' ': ([],[]),
        '_': ([0,1,2,3,4],[5,5,5,5,5]),
        '0': ([1,2,3,0,3,4,0,2,4,0,1,4,0,4,1,2,3],[0,0,0,1,1,1,2,2,2,3,3,3,4,4,5,5,5]),
        '1': ([2,1,2,2,2,2,0,1,2,3,4],[0,1,1,2,3,4,5,5,5,5,5]),
        '2': ([1,2,3,0,4,3,2,1,0,1,2,3,4],[0,0,0,1,1,2,3,4,5,5,5,5,5]),
        '3': ([1,2,3,0,4,2,3,4,0,4,1,2,3],[0,0,0,1,1,2,2,3,4,4,5,5,5]),
        '4': ([3,2,3,1,3,0,3,0,1,2,3,4,3],[0,1,1,2,2,3,3,4,4,4,4,4,5]),
        '5': ([0,1,2,3,4,0,0,1,2,3,4,0,4,1,2,3],[0,0,0,0,0,1,2,2,2,2,3,4,4,5,5,5]),
        '6': ([1,2,3,4,0,0,1,2,3,0,4,0,4,1,2,3], [0,0,0,0,1,2,2,2,2,3,3,4,4,5,5,5]),
        '7': ([0,1,2,3,4,4,3,2,1,0], [0,0,0,0,0,1,2,3,4,5]),
        '8': ([1,2,3,0,4,1,2,3,0,4,0,4,1,2,3], [0,0,0,1,1,2,2,2,3,3,4,4,5,5,5]),
        '9': ([1,2,3,0,4,1,2,3,4,4,4,4], [0,0,0,1,1,2,2,2,2,3,4,5]),
        'CLEAR': ([0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4],[0,0,0,0,0,1,1,1,1,1,2,2,2,2,2,3,3,3,3,3,4,4,4,4,4,5,5,5,5,5])
    }
    letter_coors = []
    for i, x in enumerate(locs[letter][0]):
        letter_coors.append((x, locs[letter][1][i]))
    letter_string = ''
    for coor_pair in letter_coors:
        letter_string += t.move_x(strt[0] + coor_pair[0])
        letter_string += t.move_y(strt[1] + coor_pair[1])
        letter_string += terminal.on_color(color)
        if clr_char:
            letter_string += t.normal
        letter_string += ' ' + t.normal + t.move(t.height - 2, 0)
    return letter_string

