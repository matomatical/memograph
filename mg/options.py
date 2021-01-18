import os
import argparse

# Program information:
PROGRAM = "mg"
VERSION = "0.0.3"
DESCRIP = "memograph: memorise a knowledge graph with Bayesian scheduling"

# XXX_DEFUALT default values (to use if flag is not provided)
# XXX_NOVALUE missing values (to use if flag is provided, but with no value)
NUMBER_DEFAULT = 6

# TODO: CHANGE THIS TO SOME KIND OF TOPIC LIST
# TODO: MAYBE MAKE THE SCRIPTS HAVE A .mg EXTENSION?
GRAPH_SPEC_HELP = """
knowledge graph specification format:
Knowledge graph edges (a.k.a. 'cards') are taken from .mg decks in the
current directory. Each .mg deck is a script defining a generator function
`graph()` yielding (node 1, node 2) pairs or (node 1, node 2, topic) triples.
Nodes can be primitives (str, int, float, bool) or of type `mg.graph.Node`.
"""

def get_options():
    """Parse and return command-line arguments."""
    parser = argparse.ArgumentParser(
            prog=PROGRAM,
            description=DESCRIP,
            epilog=GRAPH_SPEC_HELP,
        )
    parser.add_argument(
            '-v',
            '--version',
            action='version',
            version=f"{PROGRAM} {VERSION}"
        )
    
    # most of the action happens within one of the various subcommands:
    subparsers = parser.add_subparsers(
            dest="subcommand",
            title="subcommands",
            help="run subcommand --help for detailed usage",
        )
    # most subcommands allow for topics to be specified, as a set:
    topics_superparser = argparse.ArgumentParser(
            add_help=False,
        )
    topics_superparser.add_argument(
            'topics',
            metavar='TOPIC',
            help="topic filter (restrict to cards with this topic)",
            nargs="*",
            action=SetAction,
        )


    # # #
    # drill subcommand
    # 
    drillparser = subparsers.add_parser(
            "drill",
            parents=[topics_superparser],
            description="mg drill: practice the cards most in need of review",
            help="drill existing cards this session",
            epilog=GRAPH_SPEC_HELP,
        )
    drillparser.add_argument(
            '-n',
            '--num_cards',
            metavar="N",
            type=int,
            default=NUMBER_DEFAULT, # if the flag is not present
            help=f"number of cards in session (default {NUMBER_DEFAULT})",
        )
    drillparser.add_argument(
            '-r',
            '--reverse',
            action="store_true",
            help="reverse card sides for session",
        )
    drillparser.add_argument(
            '-m',
            '--missed',
            action="store_true",
            help="restrict to recently-failed and just-learned cards",
        )

    # # #
    # learn subcommand
    #
    learnparser = subparsers.add_parser(
            "learn",
            parents=[topics_superparser],
            description="mg learn: introduce new cards for the first time",
            help="introduce new cards for this session",
            epilog=GRAPH_SPEC_HELP,
        )
    learnparser.add_argument(
            '-n',
            '--num_cards',
            metavar="N",
            type=int,
            default=NUMBER_DEFAULT, # if the flag is not present
            help=f"number of cards in session (default: {NUMBER_DEFAULT})",
        )

    # # #
    # status subcommand
    # 
    statusparser = subparsers.add_parser(
            "status",
            parents=[topics_superparser],
            description="mg status: summarise model statistics / predictions",
            help="summarise model predictions",
        )
    statusparser.add_argument(
            '-H',
            '--histogram',
            action="store_true",
            help="histogram the expected recall probabilities",
        )
    statusparser.add_argument(
            '-P',
            '--posterior',
            action="store_true",
            help="histogram the full posterior over recall probabilities",
        )
    statusparser.add_argument(
            '-S',
            '--scatter',
            action="store_true",
            help="scatter expected recall probability against elapsed time",
        )
    statusparser.add_argument(
            '-L',
            '--list',
            action="store_true",
            help="print every card with elapsed time and expected recall",
        )
    
    # # #
    # checkup subcommand
    # 
    checkupparser = subparsers.add_parser(
            "checkup",
            parents=[topics_superparser],
            description="mg checkup: fix broken references in logs and data",
            help="fix internal broken references",
        )

    # # #
    # future commands
    # 
    subparsers.add_parser("history",   help="coming soon...")
    subparsers.add_parser("recompute", help="coming soon...")
    subparsers.add_parser("commit",    help="coming soon...")
    subparsers.add_parser("sync",      help="coming soon...")

    # # #
    # that's all, folks!
    # 
    return parser.parse_args()


class SetAction(argparse.Action):
    """
    Action to take a multiple-value argument (e.g. nargs="*" or "+") and
    store it as a set instead of a list in the namespace.
    """
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, set(values))
