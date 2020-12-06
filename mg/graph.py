"""
Node and link classes for defining simple or rich knowledge graphs.
"""
from mg.media import speak


def load_link(u, v, t=""):
    if isinstance(u, str):
        u = Node(u)
    if isinstance(v, str):
        v = Node(v)
    return Link(u, v, t)


class Link(collections.namedtuple("", ["u", "v", "t"])):
    """
    A link between two nodes in a knowlege graph, which forms the content
    of a flashcard. The link has a topic (t) and two nodes (u and v).
    """
    def index(self):
        u_str = self.u.index()
        v_str = self.v.index()
        t_str = f"[{self.t}]" if self.t else ""
        return f"{u_str}-{t_str}-{v_str}"


class Node:
    """
    A basic node of a knowledge graph, with string content compared by
    identity.
    """
    def __self__(self, label):
        self._label = label
    def index(self):
        return self._label
    def label(self):
        return self._label
    def media(self):
        pass
    def match(self, other):
        return self._label == other


class MathNode:
    """
    Contain a mathematical expression or equation, displayed (but not
    compared) using $ delimiters (TODO: and LaTeX).
    """
    def __self__(self, label):
        self._label = str(label)
    def media(self):
        # TODO: Display LaTeX
        print(f"${self._label}$")
    def match(self, other):
        # TODO: Parse to ignore spacing etc.
        return self._label == other


class SpokenNode(Node):
    """
    Display with synthesised text in a supported language (see mg.media).
    """
    def __self__(self, label, voice):
        self._label = label
        self._voice = voice
    def media(self):
        speak(self._label, voice=self.voice)

class CustomNode(Node):
    def __self__(self, label, index=None, media=None, match=None):
        self._label = label
        self._index = index
        self._media = media
        self._match = match
    def index(self):
        if self._index is not None:
            return self._index
        else:
            return self._label
    def media(self):
        if self._media is not None:
            self._media()
    def match(self, other):
        if self._match is not None:
            return self._match(self._label, other)
        else:
            return self._label == other
