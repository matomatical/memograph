import random

from mg.io import print, input


def run_learn(graph, options):
    # decide which links to introduce
    print("introduce some new links...")
    hand = graph.query(
        number=options.num_cards,
        topics=options.topics,
        new=True
    )
    n = len(hand)
    if n == 0:
        print("no new links! try drilling some old ones.")
        return
    random.shuffle(hand)

    # introduce the links
    for i, link in enumerate(hand, 1):
        print(f"<bold>**<reset> learn {i}/{n} <bold>**<reset>")
        face, back = link.u, link.v
        if link.t: print("topics:", link.t)
        print("prompt:", face.label())
        face.media()
        input("return:")
        print("answer:", back.label())
        back.media()
        instructions = "easy (g+↵) | medium (↵) | hard (h+↵)"
        rating = input("rating:", r=instructions)
        if rating == "g":
            link.m.init([1, 1,  2*24*60*60])
        elif rating == "h":
            link.m.init([1, 1,        1*60])
        else:
            link.m.init([1, 1,     1*60*60])
