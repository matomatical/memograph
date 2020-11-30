import os
import argparse

# Program information:
PROGRAM = "mg"
VERSION = "0.0.1"
DESCRIP = "drill some edges of a knowledge graph with Bayesian scheduling."

# XXX_DEFUALT default values (to use if flag is not provided)
# XXX_NOVALUE missing values (to use if flag is provided, but with no value)
NUMBER_DEFAULT = 6

GRAPH_SPEC_HELP = """
.mg direcory format:
  The .mg directory format is required to specify graphs for drilling.
  Such a directory should contain two files:
  * 'graph.py', defining a generator function 'graph()' which yields
    (topic, node 1, node 2) triples.
  * 'data.json' (created if not present; overwritten by this script)
    to store learning progress.
"""

def get_options():
    """Parse and return command-line arguments."""
    parser = argparse.ArgumentParser(
        prog=PROGRAM,
        description=DESCRIP,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=GRAPH_SPEC_HELP,
    )
    
    # positional arguments used for player package specifications:
    parser.add_argument(
        'graphs',
        metavar='GRAPH',
        help="path to a graph module, a .mg directory (see below)",
        action=GraphSpecsAction,
        nargs="+",
    )
    
    # optional arguments used for configuration:
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version=VERSION
    )
    parser.add_argument(
        '-n',
        '--num_cards',
        metavar="N",
        type=int,
        default=NUMBER_DEFAULT, # if the flag is not present
        help=f"number of cards in drill session (default: {NUMBER_DEFAULT})",
    )
    parser.add_argument(
        '-l',
        '--learn',
        action="store_true",
        help="use new cards for session",
    )
    parser.add_argument(
        '-r',
        '--reverse',
        action="store_true",
        help="reverse card sides for session",
    )
    parser.add_argument(
        '-t',
        '--topics',
        metavar="TOPIC",
        nargs='+',
        help=f"resctrict card topics for session (not implemented)",
    )
    parser.add_argument(
        '-s',
        '--status',
        action="store_true",
        help="show Bayesian status for decks",
    )
    parser.add_argument(
        '-p',
        '--preview',
        action="store_true",
        help="list cards in deck with recall probability",
    )

    try:
        return parser.parse_args()
    except FileNotFoundError as e:
        parser.error(e)

class GraphSpecsAction(argparse.Action):
    def _prep(self, path):
        if not os.path.isdir(path):
            if not path.endswith(".mg") and os.path.isdir(path+".mg"):
                path = path + ".mg"
            else:
                raise FileNotFoundError("missing .mg directory " + path)
        graph_path = os.path.join(path, "graph.py")
        data_path = os.path.join(path, "data.json")
        if not os.path.lexists(graph_path):
            raise FileNotFoundError("missing graph file " + graph_path)
        return graph_path, data_path
    def __call__(self, parser, namespace, values, option_string=None):
        # save the result in the arguments namespace as a tuple
        setattr(namespace, self.dest, [self._prep(v) for v in values])
