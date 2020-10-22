import argparse

# Program information:
PROGRAM = "mg"
VERSION = "0.0.0"
DESCRIP = "drill some edges of a knowledge graph with Bayesian scheduling."

# XXX_DEFUALT default values (to use if flag is not provided)
# XXX_NOVALUE missing values (to use if flag is provided, but with no value)
NUMBER_DEFAULT = 6

PKG_SPEC_HELP = """
To specify deck(s) for drilling, you can use any absolute module name (as
with import statements, e.g. 'module.submodule') or relative path (to a
file or directory containing the Python module, e.g. 'module/submodule' or
'module/submodule.py').
Either way, mg will attempt to import the specified package/module and then
load a list named 'deck'.
If you want mg to look for a list with some other name you can put the
alternative name after a ':' (e.g. 'module:cards' for a list named 'cards').
"""

def get_options():
    """Parse and return command-line arguments."""
    parser = argparse.ArgumentParser(
        prog=PROGRAM,
        description=DESCRIP,
        add_help=False, # <-- we will add it back to the optional group.
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    # positional arguments used for player package specifications:
    positionals = parser.add_argument_group(
        title="decks (positional argument(s))",
        description=PKG_SPEC_HELP,
    )
    positionals.add_argument(
        'decks',
        metavar='DECK',
        help="location of deck module",
        action=PackageSpecAction,
        nargs="+",
    )
    
    # optional arguments used for configuration:
    optionals = parser.add_argument_group(title="optional arguments")
    optionals.add_argument(
        '-h',
        '--help',
        action='help',
        help="show this message",
    )
    optionals.add_argument(
        '-v',
        '--version',
        action='version',
        version=VERSION
    )
    optionals.add_argument(
        '-n',
        '--num_cards',
        metavar="N",
        type=int,
        default=NUMBER_DEFAULT, # if the flag is not present
        help=f"number of cards in drill session (default: {NUMBER_DEFAULT})",
    )
    optionals.add_argument(
        '-l',
        '--learn',
        action="store_true",
        help="use new cards for session",
    )
    optionals.add_argument(
        '-r',
        '--reverse',
        action="store_true",
        help="reverse card sides for session",
    )
    optionals.add_argument(
        '-t',
        '--topics',
        metavar="TOPIC",
        nargs='+',
        help=f"resctrict card topics for session",
    )
    optionals.add_argument(
        '-s',
        '--status',
        action="store_true",
        help="show Bayesian status for decks",
    )
    optionals.add_argument(
        '-p',
        '--preview',
        action="store_true",
        help="list cards in deck(s)",
    )


    args = parser.parse_args()
    return args

class PackageSpecAction(argparse.Action):
    def _prep(self, spec):
        # detect alternative class:
        if ":" in spec:
            pkg, key = spec.split(':', maxsplit=1)
        else:
            pkg = spec
            key = "deck"
        # try to convert path to module name
        mod = pkg.strip("/").replace("/", ".")
        if mod.endswith(".py"): # NOTE: Assumes submodule is not named `py`.
            mod = mod[:-3]
        return mod, key
    def __call__(self, parser, namespace, values, option_string=None):
        # save the result in the arguments namespace as a tuple
        setattr(namespace, self.dest, [self._prep(spec) for spec in values])
