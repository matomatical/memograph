# memograph

A utility for drilling flashcards based on an online Bayesian
spaced-repetition memory model ([ebisu](https://github.com/fasiha/ebisu)).

For example decks and my memory models, see
[memograph-decks](https://github.com/matomatical/memograph-decks) repo.

## Installation

* Install Python 3.7 or higher.
* Clone this repository.
* Install requirement `ebisu` e.g. with `pip install -r requirements.txt`.
* Create some .mg directories
  (or see [memograph-decks](https://github.com/matomatical/memograph-decks)).

## Usage

Call the program with `python3 -m mg <options>` (or use an alias `mg`).

(Apologies to `mg(1)`, the 'emacs-like text editor' on unix, but I like the
name too much, and I don't see why you deserve it more than I.)

From there, see the help:

```
usage: mg [-h] [-v] [-n N] [-l] [-r] [-t TOPIC [TOPIC ...]] [-s] [-p]
          GRAPH [GRAPH ...]

drill some edges of a knowledge graph with Bayesian scheduling.

positional arguments:
  GRAPH                 path to a graph module, a .mg directory (see below)

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -n N, --num_cards N   number of cards in drill session (default: 6)
  -l, --learn           use new cards for session
  -r, --reverse         reverse card sides for session
  -t TOPIC [TOPIC ...], --topics TOPIC [TOPIC ...]
                        include cards whose topic contains these substrings
  -s, --status          show Bayesian status for decks
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

* Improve keyboard controls when an option is needed
* Add multimedia extensions:
  * Sound effects
  * Text-to-speech e.g. for language cards
  * Mathematics equations (in the terminal?!)
  * Support image-based flashcards.
* Find a nice way to allow custom assessment (autocomplete?)
* There is a noticable delay to import ebisu, which pulls numpy.
  Consider reimplementing in pure python if possible (also this will be fun!)

Eventually, long-term project goals:
* Perhaps separate `ptdb` (the plain-text database) into another project.
* Perhaps separate `topk` (the efficient heap-based top-k algorithm) into
  another project.
* Perhaps switch to a domain-specific language for specifying the graphs.
* It might be worth pulling in numpy for very large decks due to savings from
  vectorisation. Reimplement ebisu for opt-in use with more vectorisation?
* Switch to a richer, more structured memory model. I have in mind something
  like a mix between autodiff and belief nets for diagnosing missing knowledge
  based on quiz questions generated by an arbitrary program.
  The result should ideally allow generating unlimited 'quiz' questions driven
  by a finite memory model (e.g. a context-free grammar).
  The idea still needs some work.

Done:
* There is a noticable delay when printing using `prompt_toolkit`. Since my
  use case is very simple, it should be possible to replace with pure python
  using readline and ANSI codes.
  * Switch to standard readline for the input (forgo rprompt... for now!)
  * Switch to simpler, home-built formatted printing functionality
  * Reimplement right-aligned printing using '\r' and terminal width
