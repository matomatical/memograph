import random

from mg.io import print, input

def run_drill(graph, options):
    # decide which cards to drill
    print("drill some old cards...")
    hand = graph.query(number=options.num_cards, topics=options.topics)
    n = len(hand)
    if n == 0:
        print("no old cards! try learning some new ones.")
        return
    random.shuffle(hand)

    # drill the cards
    for i, link in enumerate(hand, 1):
        print(f"<bold>**<reset> drill {i}/{n} <bold>**<reset>")
        if options.reverse:
            face, back = link.v, link.u
        else:
            face, back = link.u, link.v
        if link.t: print("topics:", link.t)
        print("prompt:", face.label())
        face.media()
        guess = input("recall:")
        if back.match(guess):
            print(f"answer: <bold><green>{back.label()}<reset>")
            back.media()
            link.m.update(True)
        else:
            print(f"answer: <bold><red>{back.label()}<reset>")
            back.media()
            instructions = "forgot (↵) | got it (g+↵) | skip (s+↵)"
            commit = input("commit:", r=instructions)
            if commit == "g":
                print("<bold><green>got it!<reset>")
                link.m.update(True)
            elif commit == "s":
                link.m.review()
            else:
                link.m.update(False)

