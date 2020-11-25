import os
import sys
import time
import random
import runpy
import itertools
import collections

import ebisu

from mg import ptdb
from mg import topk

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
            l = str(card.link())
            p = card.predict(exact=True)
            print(f"{i:>4d}. {l:62s} ({p:>6.1%})")
            i += 1
        for card in deck.draw_new():
            l = str(card.link())
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



class Deck:
    def __init__(self, graph_path, data_path, reverse):
        graph = runpy.run_path(graph_path)['graph']()
        self.data = ptdb.Database(data_path)
        self.deck = []
        for link in graph:
            link = Link(*link)
            i = str(link)
            card = Card(link, self.data[i])
            if reverse:
                card.flip()
            self.deck.append(card)
    def draw_new(self, num_cards=None):
        new_deck = filter(Card.is_new, self.deck)
        return list(itertools.islice(new_deck, num_cards))
    def draw(self, num_cards=None):
        old_deck = itertools.filterfalse(Card.is_new, self.deck)
        if num_cards is None:
            return sorted(old_deck, key=Card.predict)
        return topk.topk(old_deck, num_cards, key=Card.predict, reverse=True)
    def save(self):
        self.data.save()


class Link(collections.namedtuple("Link", ["t", "u", "v"])):
    def __str__(self):
        return f"{self.u!r}-[{self.t}]-{self.v!r}"
    def __repr__(self):
        return f"Link(t={self.t!r}, u={self.u!r}, v={self.v!r})"


class Card:
    def __init__(self, link, data):
        self.l = link
        self.u = link.u
        self.v = link.v
        self.data = data
    def is_new(self):
        return self.data == {}
    def review(self):
        self.data['lastTime'] = self._current_time()
    def initialise(self, prior=[1, 1, 1*60*60]):
        self.data['priorParams'] = prior
        self.data['numDrills'] = 0
        self.data['lastTime'] = self._current_time()
    def predict(self, exact=False):
        # new card, skip
        if self.is_new():
            return None
        elapsed_time = self._current_time() - self.data['lastTime']
        prior_params = self.data['priorParams']
        return ebisu.predictRecall(prior_params, elapsed_time, exact=exact)
    def update(self, got):
        self.data['numDrills'] += 1
        now = self._current_time()
        prior_params = self.data['priorParams']
        elapsed_time = now - self.data['lastTime']
        postr_params = ebisu.updateRecall(prior_params, got, 1, elapsed_time)
        self.data['priorParams'] = postr_params
        self.data['lastTime'] = now
    def flip(self):
        self.u, self.v = self.v, self.u
    def face(self):
        return self.u
    def back(self):
        return self.v
    def link(self):
        return self.l
    def _current_time(_self):
        return int(time.time())
