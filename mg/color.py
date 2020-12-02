import collections

class RGB(collections.namedtuple("RGB", "r g b")):
    """
    Wrap a red, green, blue triple.
    """

HEXDIGITS = set("0123456789abcdefABCDEF")

def is_hex(s):
    return len(s) == 7 and s[0] == "#" and all(d in HEXDIGITS for d in s[1:])

def to_hex(rgb):
    return f"#{rgb.r:02x}{rgb.g:02x}{rgb.b:02x}"

def to_rgb(hex):
    r = int(hex[1:3], base=16)
    g = int(hex[3:5], base=16)
    b = int(hex[5:7], base=16)
    return RGB(r, g, b)

def colormap_red_green(p):
    return RGB(int(255*(1-p)), int(255*p), 0)
