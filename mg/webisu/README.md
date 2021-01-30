# *webisu*

This module is a replication of fasiha's ebisu algorithm for a Bayesian
spaced repetition system, implemented in pure Python.

I built this app as a personal project and to help remove dependencies
from my flashcard app. I imposed some of my own design choices on the
implementation, and variations compared to the original ebisu range in
scope from cosmetic to major.

The key differences are as follows:

* The API is changed, according to my own subjective preferences.
  However, the module `webisu.ebisu` provides a rough translation,
  where functionality is equivalent.
* There is an additional function returning the probability density
  for a given recall probability, which may be useful for visualising
  the deck's status.
* Binomial updates are not implemented for n > 1 (only Bernoulli trial
  updates are supported), as my flashcard app uses Bernoulli updates
  and Binomial updates required a more sophisticated safe logsumexp
  function than I have so far implemented in pure Python.
* Right now, no cache is used for beta function calls (I might later
  follow fasiha on this one).
* The update method currently does not implement any rebalancing, but
  this is a work-in-progress.
* I plan for the update method to eventually use a different approach
  to rebalancing, but this is still a work-in-progress.
