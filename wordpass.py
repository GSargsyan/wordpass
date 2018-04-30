import argparse
import math
from difflib import SequenceMatcher

from helpers import pp, NoSuchKeyError, throw


""" --- FUNCTIONS --- """

def print_kboard(pwd, shifts):
    kboard = [['_' for _ in range(c)] for c in row_key_counts]
    shifts_sum = 0
    for count, char in enumerate(pwd):
        i, j = char_position(char)
        kboard[i][j] = str(count + 1)

    for i, row in enumerate(kboard):
        shifts_sum += shifts[i]
        print('\n')
        print(' ' * (math.ceil(2 * shifts_sum) + 4) + ' '.join(row))
    print('\n')


def keys_pressed(pwd):
    kboard = [[0 for _ in range(c)] for c in row_key_counts]
    for c, char in enumerate(pwd):
        i, j = char_position(char)
        kboard[i][j] = c + 1
    return kboard


def char_position(char):
    """ Returns characters position in keys_lo or keys_hi """
    for i, row in enumerate(keys_lo):
        for j, key in enumerate(row):
            if key == char or char == keys_hi[i][j]:
                return i, j,


def _strength(password):
    """ Returns number in range [0, 1] indicating strength of the password """
    score = 1
    total_ns = 0
    for i in range(len(password) - 1):
        if password[i] == password[i + 1]:
            total_ns += 1
            continue
            
        neighbs = neighbors(password[i])
        for side, ns in neighbs.items():
            if password[i + 1] in ns:
                total_ns += 1
                break
    penalty = 0
    if total_ns != 0:
        penalty = total_ns / len(password)
    return round(score - penalty, 3)


def strength(pwd):
    pressed = keys_pressed(pwd)
    for i, row in enumerate(pressed):
        if len(set(row)) == 1:
            continue
        row_min = min([x for x in row if x != 0])
        for j, col in enumerate(row):
            if col != 0:
                pressed[i][j] -= row_min - 1
    # Trim rows
    for i, row in enumerate(pressed):
        pressed[i] = trim_zeros(row)
    score = 0
    penalty = 0
    for row in pressed:
        if len(row) < 3:
            continue
        row = [str(x) for x in row]
        for pattern, pat_pen in row_patterns.items():
            pattern = [str(x) for x in pattern[:len(row)]]
            similarity = similar(''.join(pattern), ''.join(row))
            penalty += similarity
    penalty = penalty / len(pwd)
    print("Score: " + str(1 - round(penalty, 3)))


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def trim_zeros(l):
    """ Trims starting and trailing 0's of list """
    for j in range(len(l)):
        if l[0] == 0:
            del l[0]
        else:
            break
    for j in range(len(l)):
        if l[-1] == 0:
            del l[-1]
        else:
            break
    return l

def neighbors(key):
    """ Returns dict of tuples containing neighbors of the given key on the keyboard
    raises NoSuchKeyError if the key doesn't exist in the given keyboard.
    """

    for kb in (keys_lo, keys_hi,):
        row, col = pos_in_keyboard(key, kb)
        if row is not None and row >= 0:
            kboard = kb
            break

    if row is None:
        raise NoSuchKeyError("'{}'".format(key))

    res = {}
    # LEFT key
    if col > 0:
        res['left'] = [kboard[row][col - 1]]
    # RIGHT key
    if col < len(kboard[row]) - 1:
        res['right'] = [kboard[row][col + 1]]
    # TOP keys
    if row > 0:
        res['top'] = []
        if isinstance(shifts[row], int):
            res['top'].append(kboard[row - 1][col + shifts[row]])
        else:
            if math.floor(col + shifts[row]) >= 0:
                res['top'].append(
                        kboard[row - 1][math.floor(col + shifts[row])])
            if math.ceil(col + shifts[row]) < len(kboard[row]):
                res['top'].append(
                        kboard[row - 1][math.ceil( col + shifts[row])])
    # BOTTOM keys
    if row < len(kboard) - 1:
        res['bottom'] = []
        if isinstance(shifts[row + 1], int):
            res['bottom'].append(kboard[row + 1][col - shifts[row]])
        else:
            if math.floor(col - shifts[row + 1]) >= 0:
                res['bottom'].append(
                        kboard[row + 1][math.floor(col - shifts[row + 1])])
            if math.ceil(col - shifts[row + 1]) < len(kboard[row + 1]):
                res['bottom'].append(
                        kboard[row + 1][math.ceil( col - shifts[row + 1])])

    return res


# TODO: Duplicate functions pos_in_keyboard() and char_position()
def pos_in_keyboard(key, keyboard):
    """ Return (row, col) position as tuple of key in keyboard """
    for row_num, row in enumerate(keyboard):
        if key in row:
            return (row_num, row.index(key),)
    return None, None


""" --- MAIN --- """

""" BAD KEY SEQUENCE PATTERNS AND THEIR PENALTIES """
# There is NO NEED to specift reverse order or starting character
# Penalties are integers from 1 to 10
col_patterns = {
                (1,2,3,4): 1,
                (1,3,5,7): 1,
                (1,0,2,0): 1
               }
row_patterns = {
                (1,2,3,4,5,6,7,8,9,10): 10,
                (1,3,5,7,9,11,13,15,17): 8,
                (1,4,7,10,13,16,19,22,25,28): 5,
                (1,0,2,0,3,0,4,0,5,0,6): 7,
                (1,5,9,13,17,21,25,29,33): 3
               }


""" KEYBOARD SPECIFIC VARIABLES """
keys_lo = (('`', '1' , '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '='),
                   ('q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\'),
                      ('a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'"),
                         ('z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/'))
keys_hi = (('~', '!' , '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+'),
                   ('Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '{', '}', '\|'),
                      ('A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ':', '"'),
                         ('Z', 'X', 'C', 'V', 'B', 'N', 'M', '<', '>', '?'))
row_key_counts = (13, 13, 11, 10)

"""
As letter 'q' is not directly under '`' on my keyboard
we need shifts variable
that can be specific for each keyboard.
Shifts are relative to the upper row
"""
shifts = (0, 1.5, 0.5, 0.5)
""" END KEYBOARD SPECIFIC VARIABLES """

parser = argparse.ArgumentParser(prog='python3 wordpass.py',
        description='WordPass is a tool to check password strength \
                against social engeneering attacks.')
parser.add_argument('-p', metavar='password', required=True,
        help='Password to check vulnerabilities against')
args = parser.parse_args()

password = [c for c in args.p]

if __name__ == '__main__':
    print_kboard(password, shifts)
    strength(password)
    #print("Strength: " + str(strength(password)))
