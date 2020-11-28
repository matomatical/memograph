import random

from mg.flashcards import Deck, Card
from mg.options import get_options
from mg.io import print, input
from mg.plot import print_hist
from mg.color import colormap_red_green as color


def main():
    options = get_options()
    print("<b>**</b> welcome <b>**</b>")

    # load deck
    deck = Deck(*options.graph, options.reverse)

    # run program
    if options.status:
        run_status(deck, options)
    elif options.preview:
        run_preview(deck, options)
    elif options.learn:
        run_learn(deck, options)
    else:
        run_drill(deck, options)


def run_status(deck, options):
    print("probability of recall histogram:")
    probs = [c.predict(exact=True) for c in deck.draw()]
    print_hist(probs, lo=0, hi=1, width=20, height=60, labelformat="4.0%")


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
    random.shuffle(hand)
    for card in hand:
        print("<b>**</b> <blue>NEW CARD</blue> <b>**</b>")
        print("prompt:", card.face())
        input("return:")
        print("answer:", card.back())
        rating = input("rating:", r="easy (o+↵) | medium (↵) | hard (p+↵)")
        if rating == "o":
            card.initialise([1, 1,  5*60*60])
        elif rating == "p":
            card.initialise([1, 1,     1*60])
        else:
            card.initialise([1, 1,     5*60])
    print("saving.")
    deck.save()

    
def run_drill(deck, options):
    print("drill some old cards...")
    hand = deck.draw(options.num_cards)
    random.shuffle(hand)
    for card in hand:
        print("prompt:", card.face())
        guess = input("recall:")
        if guess == card.back():
            print(f"answer: <b><green>{card.back()}</green></b>")
            card.update(True)
        else:
            print(f"answer: <b><red>{card.back()}</red></b>")
            commit = input("commit:", r="forgot (↵) | got it (o+↵) | skip (p+↵)")
            if commit == "o":
                card.update(True)
            elif commit == "p":
                card.review()
            else:
                card.update(False)
    print("saving.")
    deck.save()

