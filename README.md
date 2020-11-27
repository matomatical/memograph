# memograph

A utility for drilling flashcards based on an online Bayesian
spaced-repetition memory model ([ebisu](https://github.com/fasiha/ebisu))

## Installation

* Install Python 3.7 or higher.
* Clone this repository and cd into this dirctory.
* Install requirements `ebisu` and `prompt_toolkit`,
  e.g. with `pip install -r requirements.txt`.
* Create some .mg directories (or copy mine from another repo, forthcoming).

## Usage

Call the program with `python3 -m mg <options>` (or use an alias `mg`).

(Apologies to `mg(1)` (the 'emacs-like text editor' on unix), but I like the
name too much, and I don't see why you deserve it more than I.)

From there, see the help:

```
usage: mg [-h] [-v] [-n N] [-l] [-r] [-t TOPIC [TOPIC ...]] [-s] [-p] GRAPH

drill some edges of a knowledge graph with Bayesian scheduling.

positional arguments:
  GRAPH                 path to graph module, a .mg directory (see below)

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -n N, --num_cards N   number of cards in drill session (default: 6)
  -l, --learn           use new cards for session
  -r, --reverse         reverse card sides for session
  -t TOPIC [TOPIC ...], --topics TOPIC [TOPIC ...]
                        resctrict card topics for session (not implemented)
  -s, --status          show Bayesian status for decks (not implemented)
  -p, --preview         list cards in deck with recall probability

```

## Deck format

You can create your own flashcard decks by creating a directory in the
`.mg` format.

From the help:

```
.mg direcory format:
  The .mg directory format is required to specify graphs for drilling.
  Such a directory should contain two files:
  * 'graph.py', defining a generator function 'graph()' which yields
    (topic, node 1, node 2) triples.
  * 'data.json' (created if not present; overwritten by this script)
    to store learning progress.
```

Here is an example of a `graph.py`, which produces the names of the first
ten German numbers:

```python
D = ['null','ein','zwei','drei','vier','fünf','sechs','sieben','acht','neun']
def graph():
    for i, n in enumerate(D):
        yield ("de.num", i, n)
#              ^ optional 'topic' (can leave as "")
```

To turn this into a deck, name it something like `de.num.mg/graph.py`.
The deck will be named `de.num.mg`, you can then drill it using the
example command:

```
% mg de.num
```

This format is not considered stable.

## TODO list

* Implement 'Bayesian deck status' command to show a snapshot of memory for
  a whole deck (maybe including my own implementation of `termplotlib`).
* Improve keyboard controls when an option is needed
* Add multimedia extensions:
  * Sound effects
  * Text-to-speech e.g. for language cards
  * Mathematics equations (in the terminal?!)
  * Support image-based flashcards.
* Find a nice way to allow custom assessment (autocomplete?)

Eventually, long-term project goals:
* Install as executable so that we can just run it with `mg <deck>`.
* Add example decks to repo
* Separate `ptdb` (the plain-text database) into another project.
* Separate `topk` (the efficient heap-based top-k algorithm) into another
  project.
* Reimplement `ebisu` (for fun and either vectorisation or no numpy).
* Perhaps switch to a domain-specific language for specifying the graphs.
* Switch to a richer, more structured memory model. I have in mind something
  like a mix between autodiff and belief nets for diagnosing issues. The
  result should ideally allow generating unlimited 'quiz' questions driven
  by a finite memory model. The idea still needs some work.

