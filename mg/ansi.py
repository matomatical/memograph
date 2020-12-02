import collections

from mg.color import is_hex, to_rgb

def to_ansi_code(a):
    """
    Convert a keyword to an ansi escape code, e.g. 'red' to '\\033[31m'
    or 'reset' to '\\033[0m' or '#ffffff' to '\\033[38;5;231m'.
    """
    if a in BASIC_CODES:
        return esc(BASIC_CODES[a])
    if is_hex(a):
        return esc(f"38;5;{to_216(to_rgb(a))}")
        # TODO: Add bg colors
    raise UnknownANSIKeywordException(a)

BASIC_CODES = {
        'reset':      '0',
        'bold':       '1',
        'faint':      '2',
        'italic':     '3',
        'black':     '30',
        'red':       '31',
        'green':     '32',
        'yellow':    '33',
        'blue':      '34',
        'magenta':   '35',
        'cyan':      '36',
        'white':     '37',
        'b-black':   '90',
        'b-red':     '91',
        'b-green':   '92',
        'b-yellow':  '93',
        'b-blue':    '94',
        'b-magenta': '95',
        'b-cyan':    '96',
        'b-white':   '97',
        # TODO: Add bg colors
    }

def esc(code):
    return f"\033[{code}m"

class UnknownANSIKeywordException(Exception):
    """Unknown tag or similar formatted string error"""

def to_216(rgb):
    # https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit
    r = rgb.r // 43
    g = rgb.g // 43
    b = rgb.b // 43
    return 16 + 36*r + 6*g + b
