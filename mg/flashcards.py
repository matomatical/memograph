import re
import time
import runpy
import itertools
import collections

import ebisu

from mg import ptdb
from mg import topk

from mg.graph import load_link

class Deck:
    """
    A collection of flashcards, from which one can draw unseen or at-risk
    cards for review
    """
    def __init__(self, graph_specs, reverse=False, topics=None):
        self.deck = []
        self.news = []
        self.dbs = []
        for graph_path, data_path in graph_specs:
            # load the knowledge graph's links and their memory parameters
            graph = runpy.run_path(graph_path)['graph']()
            data = ptdb.Database(data_path)
            # wrap each link in a flashcard
            for uvt in graph:
                link = load_link(*uvt)
                if topics is not None:
                    if not any(t in link.t for t in topics):
                        continue
                card = Card(link, data[link.index()])
                if reverse:
                    card.flip()
                if card.is_new():
                    self.news.append(card)
                else:
                    self.deck.append(card)
            self.dbs.append(data)
    
    def num_new(self):
        """get the number of cards that have not been seen upon load"""
        return len(self.news)
    
    def num_old(self):
        """get the number of cards that have been seen upon load"""
        return len(self.deck)

    def draw_new(self, num_cards=None):
        """
        Draw the next num_cards cards from the unseen part of the deck
        """
        return list(itertools.islice(self.news, num_cards))

    def draw(self, num_cards=None):
        """
        Draw the num_cards most at-risk cards from the deck
        """
        if num_cards is None:
            return sorted(self.deck, key=Card.predict)
        return topk.topk(self.deck, num_cards, key=Card.predict, reverse=True)

    def save(self):
        """
        Commit changes to the database
        """
        for data in self.dbs:
            data.save()

PARENS = re.compile(r"\s*\([^)]*\)")
def simplify(string):
    return PARENS.sub("", string)

class Card:
    """
    A flashcard, representing a knowledge graph link and also maintaining
    the memory model's parameter's for that card.
    """
    def __init__(self, link, data):
        self.l = link
        self.u = link.u
        self.v = link.v
        self.data = data
    
    def is_new(self):
        """bool: the card is yet to be initialised"""
        return self.data == {}
    
    def initialise(self, prior_params=[1, 1, 1*60*60], num_drills=0):
        """set the memory model"""
        self.data['priorParams'] = prior_params
        self.data['numDrills'] = num_drills
        self.data['lastTime'] = self._current_time()

    def review(self):
        """update time without updating memory model"""
        self.data['lastTime'] = self._current_time()
    
    def predict(self, exact=False):
        """
        compute the expected (log) probability of recalling the card
        note: must be initialised
        """
        # new card, skip
        elapsed_time = self._current_time() - self.data['lastTime']
        prior_params = self.data['priorParams']
        return ebisu.predictRecall(prior_params, elapsed_time, exact=exact)

    def update(self, got):
        """
        update the memory model based on the result of a drill
        note: must be initialised
        """
        self.data['numDrills'] += 1
        now = self._current_time()
        prior_params = self.data['priorParams']
        elapsed_time = now - self.data['lastTime']
        postr_params = ebisu.updateRecall(prior_params, got, 1, elapsed_time)
        self.data['priorParams'] = postr_params
        self.data['lastTime'] = now

    def flip(self):
        """reverse the front and back of the card (same memory model)"""
        self.u, self.v = self.v, self.u
    
    def face(self):
        """front of the card"""
        return self.u
    
    def back(self):
        """back of the card"""
        return self.v

    def link(self):
        """the link itself (note: same link returned upon flip)"""
        return self.l

    def grade(self, guess):
        return simplify(self.back()) == simplify(guess)
    
    def _current_time(_self):
        return int(time.time())

    def __str__(self):
        card = f"{self.face()}--{self.back()}"
        if self.is_new():
            return card
        else:
            elapsed_time = self._current_time() - self.data['lastTime']
            return f"{card} [{elapsed_time}s ago]"

