import random

from mg.io import print, input

def run_drill(deck, options):
    # decide which cards to drill
    if options.missed:
        print("drill some tough/fresh cards...")
        hand = [c for c in deck.draw() if not c.is_recalled()]
        hand = hand[:options.num_cards]
    else:
        print("drill some old cards...")
        hand = deck.draw(options.num_cards)
    n = len(hand)
    if n == 0:
        print("no old cards! try learning some new ones.")
        return
    random.shuffle(hand)

    # drill the cards
    for i, card in enumerate(hand, 1):
        print(f"<bold>**<reset> drill {i}/{n} <bold>**<reset>")
        if options.reverse:
            back, face = card
        else:
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

