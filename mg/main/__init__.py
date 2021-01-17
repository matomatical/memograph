from mg.io import print, input
from mg.plot import print_hist
from mg.color import colormap_red_green as color, to_hex
from mg.options import get_options
from mg.flashcards import Deck, Card

from mg.main.status import run_status
from mg.main.drill  import run_drill
from mg.main.learn  import run_learn

def main():
    # parse command-line input
    options = get_options()
    print("<bold>**<reset> welcome <bold>**<reset>")

    # now load cards, filtering for graph stuff
    deck = Deck(options.graphs, reverse=False, topics=None)

    # run program
    try:
        if options.subcommand == "status":
            run_status(deck, options)
        elif options.subcommand == "drill":
            run_drill(deck, deck.draw(options.num_cards))
        elif options.subcommand == "learn":
            run_learn(deck, deck.draw_new(options.num_cards))
    except (EOFError, KeyboardInterrupt):
        print("\nbye! (not saving.)")