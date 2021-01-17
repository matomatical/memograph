from glob import glob

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

    # now load cards, filtering for provided topics
    graphs = [(g+"/graph.py", g+"/data.json") for g in glob('*.mg')]
    deck = Deck(graphs, topics=options.topics)

    # run program
    try:
        if options.subcommand == "status":
            run_status(deck, options)
        elif options.subcommand == "drill":
            run_drill(deck, options)
            print("saving.")
            deck.save()
        elif options.subcommand == "learn":
            run_learn(deck, options)
            print("saving.")
            deck.save()
    except KeyboardInterrupt:
        print("\nbye! (saving.)")
        deck.save()
    except EOFError:
        print("\nbye! (not saving.)")
