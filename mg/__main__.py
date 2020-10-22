import sys
import random
import importlib

from mg.options import get_options
from mg.audio import sound

def main():
    options = get_options()

    if options.preview:
        # preview decks:
        for dpath in options.decks:
            print('.'.join(dpath))
            for card in import_deck(*dpath):
                print(repr(card))
            print()

    if options.status:
        # display status:
        for dpath in options.decks:
            print('.'.join(dpath))
            print('(status)\n')

    if not options.status and not options.preview:
        # play game:
        deck = [c for dpath in options.decks for c in import_deck(*dpath)]
        n = min(options.num_cards, len(deck))
        hand = random.sample(deck, n)
        if options.reverse: hand = [c.flip() for c in hand]
        random.shuffle(hand)

        # play!
        train(hand)

def import_deck(package_name, deck_name):
    module = importlib.import_module(package_name)
    deck = getattr(module, deck_name)
    return deck

def train(cards):
    # begin: ensure load sound
    sound('streak')
    # loop: train cards
    report = [False] * len(cards)
    i = 0
    while not all(report):
        if not report[i]:
            report[i] = play(cards[i])
        i = (i + 1) % len(cards)
    # end: display report
    print("complete!")
    print(report)
    sound('heart')

def play(card):
    print("topics:", card.t)
    print("prompt:", card.u)
    answer = input("guess?: ")
    result = card.v == answer
    if result:
        print("result: right!") # TODO: bold green
        sound("right")
    else:
        print("result: wrong!") # TODO: bold red
        sound("wrong")
        print("answer:", card.v)
    print("---")
    return result

main()
