"""
Node and link classes for defining simple or rich knowledge graphs.
"""
from mg.media import speak


# # #
# Flexible representation of nodes
# 

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
    def __hash__(self):
        return hash(self.index_str)
    def __eq__(self, other):
        return self.index_str == other.index_str


# These types are allowed in links (they will be cast as Nodes)
PRIMITIVE = (str, int, float, bool)


def load_node(n):
    if isinstance(n, PRIMITIVE):
        return Node(str(n))
    elif isinstance(n, Node):
        return n
    raise ValueError(f"link node must be mg.graph.Node or {PRIMITIVE}")

