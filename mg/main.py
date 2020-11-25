from mg.flashcards import Deck, Card
from mg.options import get_options

def main():
    options = get_options()
    print("** welcome! **")

    # load deck
    deck = Deck(*options.graph, options.reverse)

    # run program
    if options.status:
        print("status feature not yet implemented")
    elif options.preview:
        print("cards (probability of recall):")
        i = 1
        for card in deck.draw():
            l = str(card)
            p = card.predict(exact=True)
            print(f"{i:>4d}. {l:62s} ({p:>6.1%})")
            i += 1
        for card in deck.draw_new():
            l = str(card)
            print(f"{i:>4d}. {l:62s} (unseen)")
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
    print("** NEW CARD **")
    print("prompt:", card.face())
    input("return: ")
    print("answer:", card.back())
    print("okay (o+return);  medium (return);  difficult (p+return)")
    rating = input("rating: ")
    if rating == "o":
        card.initialise([1, 1,  5*60*60])
    elif rating == "p":
        card.initialise([1, 1,     1*60])
    else:
        card.initialise([1, 1,     5*60])

def drill(card):
    print("prompt:", card.face())
    guess = input("recall: ")
    print("answer:", card.back())
    if guess == card.back():
        card.update(True)
    else:
        print("forgot it (return);  got it (o+return);  skip (p+return)")
        commit = input("commit: ")
        if commit == "o":
            card.update(True)
        elif commit == "p":
            card.review()
        else:
            card.update(False)
