"""
Node and link classes for defining simple or rich knowledge graphs.
"""
import re
import collections

from mg.media import speak

PRIMITIVE = (str, int, float, bool)

def load_link(u, v, t=""):
    if isinstance(u, PRIMITIVE):
        u = Node(str(u))
    if isinstance(v, PRIMITIVE):
        v = Node(str(v))
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
    A custom node of a knowledge graph, with flexible/independent
    string content for indexing, display, comparison, and (optional)
    vocalisation.
    """
    def __init__(
                self,
                index_str,
                match_str=None,
                print_str=None,
                speak_str=None,
                speak_voice=None,
            ):
        index_str = str(index_str)
        self.index_str = index_str
        if match_str is None:
            self.match_str = index_str
        else:
            self.match_str = str(match_str)
        if print_str is None:
            self.print_str = index_str
        else:
            self.print_str = str(print_str)
        if speak_str is None:
            self.speak_str = None
        else:
            self.speak_str = str(speak_str)
        self.speak_voice = speak_voice
        self.num = None
    def index(self):
        return self.index_str
    def label(self):
        if self.num is not None:
            return f"{self.print_str} ({self.num})"
        else:
            return self.print_str
    def match(self, other):
        return self.match_str == other
    def media(self):
        if self.speak_str is not None:
            speak(self.speak_str, voice=self.speak_voice)
    def setnum(self, num):
        self.num = num
