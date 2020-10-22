# card internal representation
# aim: represent an RDF triple but with flexible display options

class Link:
    def __init__(self, t, u, v):
        self.t = t # topic(s)
        self.u = u # prompt
        self.v = v # answer
    def flip(self):
        t = self.t[:-4] if self.t.endswith('.rev') else (self.t + '.rev')
        return Link(t, self.v, self.u)
    def __repr__(self):
        return f"{self.u!r} --[{self.t}]--> {self.v!r}"
    def __hash__(self):
        return hash(repr(self))
    def __eq__(self, other):
        return repr(self) == repr(other)

class BasicNode:
    """basically wraps a string (can just use string instead)"""
    def __init__(self, text):
        self.text = text
    def __eq__(self, other):
        """used for assessing answers (other is a string)"""
        return self.text == other
    def __str__(self):
        """used for prompting or revealing answers"""
        return self.text
    def __repr__(self):
        """used while computing unique link id string"""
        return repr(self.text)

class MathNode:
    def __init__(self, expr):
        self.expr = expr
        self.text = f"${expr}$"
    def __eq__(self, other):
        return self.expr == other
    def __str__(self):
        return self.text
    def __repr__(self):
        return self.text
