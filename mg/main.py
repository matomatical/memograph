import random

from mg.flashcards import Deck, Card
from mg.options import get_options
from mg.io import print, input

def main():
    options = get_options()
    print("<b>**</b> welcome <b>**</b>")

    # load deck
    deck = Deck(*options.graph, options.reverse)

    # run program
    if options.status:
        print("<yellow>status feature not yet implemented</yellow>")

    elif options.preview:
        print("cards (probability of recall):")
        i = 1
        for card in deck.draw():
            l = str(card)
            p = card.predict(exact=True)
            t1, t2 = color(p)
            print(f"<b>{i:>4d}.</b> {l:62s} ({t1}{p:>6.1%}{t2})")
            i += 1
        for card in deck.draw_new():
            l = str(card)
            print(f"<b>{i:>4d}.</b> {l:62s} (<grey>unseen</grey>)")
            i += 1

    elif options.learn:
        print("introduce some new cards...")
        hand = deck.draw_new(options.num_cards)
        random.shuffle(hand)
        for card in hand:
            intro(card)
        print("saving.")
        deck.save()

    else:
        print("drill some old cards...")
        hand = deck.draw(options.num_cards)
        random.shuffle(hand)
        for card in hand:
            drill(card)
        print("saving.")
        deck.save()


def intro(card):
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


def drill(card):
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


def color(p):
    if p < 0.25:
        return "<b><red>", "</red></b>"
    if p < 0.5:
        return "<red>", "</red>"
    if p < 0.75:
        return "<yellow>", "</yellow>"
    if p < 0.90:
        return "<green>", "</green>"
    return "<b><green>", "</green></b>"
