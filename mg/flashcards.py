import os
import re
import glob
import time
import runpy
import itertools
import collections

import ebisu

from mg import ptdb
from mg import topk

from mg.graph import load_link

# ensure mgdata directory exists
# TODO: This really does NOT BELONG here
if not os.path.isdir("mgdata"):
    os.mkdir("mgdata")


class Deck:
    """
    A collection of flashcards, from which one can draw unseen or at-risk
    cards for review
    """
    def __init__(self, topics=set()):
        deck_paths = glob.glob('*.mg') # TODO: Allow configure?
        self.deck = []
        self.news = []
        allcards = []
        self.dbs = []
        for path in deck_paths:
            # load the knowledge graph's links and their memory parameters
            graph = runpy.run_path(path)['graph']()
            data = ptdb.Database(os.path.join("mgdata", path+".json"))
            # wrap each link in a flashcard
            for uvt in graph:
                link = load_link(*uvt)
                card = Card(link, data[link.index()])
                if not (topics <= card.topics()):
                    continue
                if card.is_new():
                    self.news.append(card)
                else:
                    self.deck.append(card)
                allcards.append(card)
            self.dbs.append(data)
        # number duplicate nodes
        for side in [Card.face, Card.back]:
            nodes = {}
            for card in allcards:
                node = side(card)
                index = node.index()
                if index in nodes:
                    nodes[index].append(node)
                else:
                    nodes[index] = [node]
            for index in nodes:
                if len(nodes[index]) > 1:
                    for i, node in enumerate(nodes[index], 1):
                        node.setnum(i)
    
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

class Card:
    """
    A flashcard, representing a knowledge graph link and also maintaining
    the memory model's parameter's for that card.
    """
    def __init__(self, link, data):
        self.link = link
        self.data = data

    def topics(self):
        return set(self.link.t.split("."))

    def face(self):
        return self.link.u

    def back(self):
        return self.link.v

    def __iter__(self):
        yield self.link.u
        yield self.link.v
    
    def is_new(self):
        """bool: the card is yet to be initialised"""
        return self.data == {}
    
    def is_recalled(self):
        if 'lastResult' in self.data:
            return self.data['lastResult']
        return None
    
    def initialise(self, prior_params=[1, 1, 1*60*60]):
        """set the memory model"""
        self.data['priorParams'] = prior_params
        self.data['numDrills'] = 0
        self.data['lastTime'] = self._current_time()
        self._log("LEARN", prior=prior_params)

    def review(self):
        """update time without updating memory model"""
        self.data['lastTime'] = self._current_time()
        self._log("REVIEW")
    
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
        self.data['lastResult'] = got
        now = self._current_time()
        prior_params = self.data['priorParams']
        elapsed_time = now - self.data['lastTime']
        postr_params = ebisu.updateRecall(prior_params, got, 1, elapsed_time)
        self.data['priorParams'] = postr_params
        self.data['lastTime'] = now
        self._log("DRILL", got=got)

    def _current_time(_self):
        return int(time.time())

    def _log(self, event, **data):
        # TODO: COMPLETELY OVERHAUL THIS WHOLE CARD AND DECK SYSTEM IT'S SHIT
        import json
        with open("mgdata/log.jsonl", 'a') as file:
            line = json.dumps({
                    'id': self.link.index(),
                    'time': self._current_time(),
                    'event': event.upper(),
                    'data': data
                })
            print(line, file=file)


    def __str__(self):
        card = f"{self.link.u.index()}--{self.link.v.index()}"
        if self.is_new():
            return card
        else:
            elapsed_time = self._current_time() - self.data['lastTime']
            return f"{card} [{elapsed_time}s ago]"

