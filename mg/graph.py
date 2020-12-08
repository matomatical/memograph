"""
Node and link classes for defining simple or rich knowledge graphs.
"""
import re
import collections

from mg.media import speak

PRIMITIVE = (str, int, float)

def load_link(u, v, t=""):
    if isinstance(u, PRIMITIVE):
        u = Node(u)
    if isinstance(v, PRIMITIVE):
        v = Node(v)
    return Link(u, v, t)


class Link(collections.namedtuple("Link", ["u", "v", "t"])):
    """
    A link between two nodes in a knowlege graph, which forms the content
    of a flashcard. The link has a topic (t) and two nodes (u and v).
    """
    def index(self):
        u_str = self.u.index()
        v_str = self.v.index()
        t_str = f"[{self.t}]" if self.t else ""
        return f"{u_str}-{t_str}-{v_str}"



PARENTHESES = re.compile(r"\s*\([^)]*\)")

class Node:
    """
    A basic node of a knowledge graph, with string content compared by
    identity.
    """
    def __init__(self, label):
        self._full_label = str(label)
        self._label = PARENTHESES.sub("", self._full_label)
    def index(self):
        return self._label
    def label(self):
        return self._full_label
    def short(self):
        return self._label
    def media(self):
        pass
    def match(self, other):
        return self._label == other


class MathNode(Node):
    """
    Contain a mathematical expression or equation, displayed (but not
    compared) using $ delimiters (TODO: and LaTeX).
    """
    def media(self):
        # TODO: Display LaTeX
        print(f"${self.short()}$")


class SpokenNode(Node):
    """
    Display with synthesised text in a supported language (see mg.media).
    """
    def __init__(self, label, text=None, voice=None):
        super().__init__(label)
        self._voice = voice if voice is not None else "en"
        self._text  = text if text is not None else self.short()
    def media(self):
        speak(self._text, voice=self._voice)

class CustomNode(Node):
    def __init__(self, label, index=None, media=None, match=None):
        self._label = label
        self._index = index
        self._media = media
        self._match = match
    def index(self):
        if self._index is not None:
            return self._index
        return super().index()
    def media(self):
        if self._media is not None:
            self._media()
    def match(self, other):
        if self._match is not None:
            return self._match(self.short(), other)
        return super().match(other)
