
def graph():
    for n in range(256):
        yield (
            "math.8b",
            BaseNode(format(n, 'd'),  10),
            BaseNode(format(n, '08b'), 2),
        )

class BaseNode:
    """display base with leading 0s and a subscript but ignore for marking"""
    def __init__(self, numstr, base):
        self.numstr = numstr
        self.basech = {2: '2', 10: 'a'}[base]
    def __eq__(self, other):
        if '_' in other:
            other = other[:other.index('_')]
        return self.numstr.lstrip('0') == other.lstrip('0')
    def __str__(self):
        return f"${self.numstr}_{self.basech}$"
    def __repr__(self):
        return str(self)

