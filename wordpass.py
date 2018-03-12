import argparse
import math

from helpers import pp, NoSuchKeyError, throw


""" --- FUNCTIONS --- """
def strength(password):
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


def pos_in_keyboard(key, keyboard):
    """ Return (row, col) position as tuple of key in keyboard """
    for row_num, row in enumerate(keyboard):
        if key in row:
            return (row_num, row.index(key),)
    return None, None


""" --- MAIN --- """

""" KEYBOARD SPECIFIC VARIABLES """
keys_lo = (('`', '1' , '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '='),
                   ('q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\'),
                      ('a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'"),
                         ('z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/'))
keys_hi = (('~', '!' , '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+'),
                   ('Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '{', '}', '\|'),
                      ('A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ':', '"'),
                         ('Z', 'X', 'C', 'V', 'B', 'N', 'M', '<', '>', '?'))
"""
As letter 'q' is not directly under '`' on my keyboard
we need shifts variable
that can be unique for each keyboard.
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
    print("Strength: " + str(strength(password)))
