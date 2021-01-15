import random

from mg.io import print, input
from mg.plot import print_hist
from mg.color import colormap_red_green as color, to_hex
from mg.options import get_options
from mg.flashcards import Deck, Card

def main():
    options = get_options()
    print("<bold>**<reset> welcome <bold>**<reset>")

    # load deck
    deck = Deck(options.graphs, options.reverse, options.topics)

    # run program
    try:
        if options.status:
            run_status(deck)
        elif options.preview:
            run_preview(deck)
        elif options.missed:
            run_drill(deck, [c for c in deck.draw() if not c.is_recalled()])
        elif options.learn:
            run_learn(deck, deck.draw_new(options.num_cards))
        else:
            run_drill(deck, deck.draw(options.num_cards))
    except (EOFError, KeyboardInterrupt):
        print("\nbye! (not saving.)")


def run_status(deck):
    n_seen  = deck.num_old()
    n_new   = deck.num_new()
    n_total = n_seen + n_new
    if n_total == 0:
        print("no cards! try adding some or changing the topic.")
        return
    if n_seen:
        print("probability of recall histogram:")
        probs = [c.predict(exact=True) for c in deck.draw()]
        print_hist(probs, lo=0, hi=1, bins=20, height=56, labelformat="4.0%")
    print(
        f"{n_seen} cards seen ({n_seen/n_total:.0%}),",
        f"{n_new} cards unseen ({n_new/n_total:.0%})"
    )

def run_preview(deck):
    print("cards (probability of recall):")
    i = 1
    for card in deck.draw():
        p = card.predict(exact=True)
        c = to_hex(color(p))
        print(f"<bold>{i:>4d}.<reset>", card, r=f"(<{c}>{p:>6.1%}<reset>)")
        i += 1
    for card in deck.draw_new():
        print(f"<bold>{i:>4d}.<reset>", card, r="(<faint>unseen<reset>)")
        i += 1

def run_learn(deck, hand):
    print("introduce some new cards...")
    n = len(hand)
    if n == 0:
        print("no new cards! try drilling some old ones.")
        return
    random.shuffle(hand)
    for i, card in enumerate(hand, 1):
        print(f"<bold>**<reset> learn {i}/{n} <bold>**<reset>")
        face, back = card
        if card.topics(): print("topics:", card.topics())
        print("prompt:", face.label())
        face.media()
        input("return:")
        print("answer:", back.label())
        back.media()
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

    
def run_drill(deck, hand):
    print("drill some old cards...")
    n = len(hand)
    if n == 0:
        print("no old cards! try learning some new ones.")
        return
    random.shuffle(hand)
    for i, card in enumerate(hand, 1):
        print(f"<bold>**<reset> drill {i}/{n} <bold>**<reset>")
        face, back = card
        if card.topics(): print("topics:", card.topics())
        print("prompt:", face.label())
        face.media()
        guess = input("recall:")
        if back.match(guess):
            print(f"answer: <bold><green>{back.label()}<reset>")
            back.media()
            card.update(True)
        else:
            print(f"answer: <bold><red>{back.label()}<reset>")
            back.media()
            instructions = "forgot (↵) | got it (g+↵) | skip (s+↵)"
            commit = input("commit:", r=instructions)
            if commit == "g":
                print("<bold><green>got it!<reset>")
                card.update(True)
            elif commit == "s":
                card.review()
            else:
                card.update(False)
    print("saving.")
    deck.save()

