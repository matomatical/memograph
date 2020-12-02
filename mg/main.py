import random

from mg.io import print, input
from mg.plot import print_hist
from mg.color import colormap_red_green as color
from mg.options import get_options
from mg.flashcards import Deck, Card


def main():
    options = get_options()
    print("<b>**</b> welcome <b>**</b>")

    # load deck
    deck = Deck(options.graphs, options.reverse, options.topics)

    # run program
    try:
        if options.status:
            run_status(deck, options)
        elif options.preview:
            run_preview(deck, options)
        elif options.learn:
            run_learn(deck, options)
        else:
            run_drill(deck, options)
    except KeyboardInterrupt:
        print("\nbye! (not saving.)")


def run_status(deck, options):
    n_seen  = len(deck.draw())
    n_new   = len(deck.draw_new())
    n_total = n_seen + n_new
    if n_seen:
        print("probability of recall histogram:")
        probs = [c.predict(exact=True) for c in deck.draw()]
        print_hist(probs, lo=0, hi=1, width=20, height=56, labelformat="4.0%")
    print(
        f"{n_seen} cards seen ({n_seen/n_total:.0%}),",
        f"{n_new} cards unseen ({n_new/n_total:.0%})"
    )

def run_preview(deck, options):
    print("cards (probability of recall):")
    i = 1
    for card in deck.draw():
        l = str(card)
        p = card.predict(exact=True)
        c = color(p)
        print(f"<b>{i:>4d}.</b> {l:62s} (<style fg='{c}'>{p:>6.1%}</style>)")
        i += 1
    for card in deck.draw_new():
        l = str(card)
        print(f"<b>{i:>4d}.</b> {l:62s} (<grey>unseen</grey>)")
        i += 1


def run_learn(deck, options):
    print("introduce some new cards...")
    hand = deck.draw_new(options.num_cards)
    n = len(hand)
    if n == 0:
        print("no new cards! try drilling some old ones.")
        return
    random.shuffle(hand)
    for i, card in enumerate(hand, 1):
        print(f"<b>**</b> learn {i}/{n} <b>**</b>")
        print("prompt:", card.face())
        input("return:")
        print("answer:", card.back())
        instructions = "easy (g+↵) | medium (↵) | hard (h+↵)"
        rating = input("rating:", r=instructions)
        if rating == "g":
            card.initialise([1, 1,  2*24*60*60])
        elif rating == "h":
            card.initialise([1, 1,        1*60])
        else:
            card.initialise([1, 1,     1*60*60])
    print("saving.")
    deck.save()

    
def run_drill(deck, options):
    print("drill some old cards...")
    hand = deck.draw(options.num_cards)
    n = len(hand)
    if n == 0:
        print("no old cards! try learning some new ones.")
        return
    random.shuffle(hand)
    for i, card in enumerate(hand, 1):
        print(f"<b>**</b> drill {i}/{n} <b>**</b>")
        print("prompt:", card.face())
        guess = input("recall:")
        if card.grade(guess):
            print(f"answer: <b><green>{card.back()}</green></b>")
            card.update(True)
        else:
            print(f"answer: <b><red>{card.back()}</red></b>")
            instructions = "forgot (↵) | got it (g+↵) | skip (s+↵)"
            commit = input("commit:", r=instructions)
            if commit == "g":
                print("<b><green>got it!</green></b>")
                card.update(True)
            elif commit == "s":
                card.review()
            else:
                card.update(False)
    print("saving.")
    deck.save()

