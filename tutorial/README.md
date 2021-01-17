# memograph tutorial

A brief guide on creating decks of flashcards and using them with
the `mg` utility.

Throughout, we will work with an example flashcard deck consisting
of the German names of the numbers 0 through 9.

The final version of the deck we build in this tutorial is included,
see [de.digits.mg](de.digits.mg/).

## Contents

Steps:

* [Step 1: Create a deck](#step-1-create-a-deck)
* [Step 2: Learn a deck](#step-2-learn-a-deck)
* [Step 3: Inspect deck status](#step-3-inspect-deck-status)
* [Step 4: Drill a deck](#step-4-drill-a-deck)
* [Step 5: Customising nodes](#step-5-customising-nodes)
  * [Terminology: Nodes, Links, Knowledge Graph](#terminology-nodes-links-knowledge-graph)
  * [Topics](#topics)
  * [Custom display and comparison strings](#custom-display-and-comparison-strings)
  * [Text-to-Speech](#text-to-speech)
  * [Duplicate nodes](#duplicate-nodes)
* [Step 6: Modifying a deck after learning](#step-6-modifying-a-deck-after-learning)

## Step 1: Create a deck

> #### Warning:
> 
> This deck format is not considered stable; it might change with future
> commits to this repository as this application matures.

From any directory you like, make a new `.mg` file. This will constitute
your flashcard deck on the filesystem.

```
$ touch de.digits.mg
```

Despite its extension, this file is really a Python script.
The script's job is to *generate flashcards*.
Flashcards are to be represented as two-tuples containing the 'front' of
the card followed by the 'back' of the card. Each 'side' of the card can
be a string, integer, float, or boolean value, and these value will be the
ones shown when you are later learning and practising the flashcards.

The entry point to the script is a Python generator function called
`graph`. `graph` should yield all of the flashcard tuples in the deck.
Thus, a very simple script for our German digits could read:

```python
def graph():
    yield 0, "null"
    yield 1, "eins"
    yield 2, "zwei"
    yield 3, "drei"
    yield 4, "vier"
    yield 5, "fünf"
    yield 6, "sechs"
    yield 7, "sieben"
    yield 8, "acht"
    yield 9, "neun"
```

Using Python to generate flashcards gives us the full power of the
language in specifying your list of flashcards.
In some cases, we might want to leverage this additional expressive
power to avoid some typing.
Here's an example equivalent to the above script:

```python
D = ['null','eins','zwei','drei','vier','fünf','sechs','sieben','acht','neun']
def graph():
    for i, n in enumerate(D):
        yield i, n
```

For such a simple deck, we haven't improved maintainability or readability
by a lot: The original script was already pretty clear and simple.
But for larger decks, or for decks where the content itself follows
some latent structure, we might want to take advantage of Python's power.
For example:

* The first *100* German numbers have a simple compositional structure
  which could be captured with a few loops and some string construction.
* Mathematical flashcards (e.g. for drilling multiplication tables,
  square/cubic numbers, factorials, combinations, binary/decimal
  conversions) can be specified very compactly with these expressions
  evaluated at run-time, rather than flashcard-creation time.
* Flashcards for cyphers such as ROT-13 can be similarly computed at
  runtime and very compactly using Python's string/char manipulation
  utilities.

Anyway, it's up to you how to make your `graph` function, `mg` just
needs it to yield a bunch of flashcard tuples.

In [Step 5](#step-5-customising-nodes), we'll learn how to enhance
these flashcard tuples with custom strings for prompting, comparison,
and even *text-to-speech*!

## Step 2: Learn a deck

Now that we have a deck, it's time to learn its cards! We'll use the `mg`
in *learn mode* for this.

Inside the same directory as our deck (Python script) `de.digits.mg`, and 
with an alias for the memograph script called `mg`
(see the installation and usage sections of the main README file),
run the following command to begin the learning session:

```
$ mg learn
```

`mg` will look for decks (`.mg` files) in the current directory and load
the cards from the generator function.

Then `mg` will begin the learning session. It will randomly order the
first six (by default, see `--num_cards` flag) cards from the generator
and introduce them one by one. For example, you might see:

```
** welcome **
introduce some new cards...
** learn 1/6 **
prompt: 4
return:
```

The front of this card is '4', and the 'return:' instruction tells you to
press the return key to see the answer. Then you will see:

```
answer: vier
rating:                                   easy (g+↵) | medium (↵) | hard (h+↵)
```

`mg` has told you that the back of this card is 'vier'. Then it asks you for
an estimate of how difficult this card will initially be for you to remember.
For example, you might have already known this one, or maybe this is the
first time you are seeing it. `mg` will use your rating to set the initial
memory model parameters for the card.

Type `g` (easy), nothing (medium), or `h` (hard) and press return.

Repeat this for all of the cards in the learning session.
Note that progress is saved at the end of each session.

Run further learning sessions if you want to learn more cards right
now---for the rest of this tutorial, I will continue with just these
first six cards learned, and the rest unseen.

## Step 3: Inspect deck status

After learning these flashcards, they will likely be fresh in your mind.
`mg` uses an exponential-decay-based Bayesian memory model where the
chance of forgetting a card increases over time, and your successes and
fails with the card help to refine an estimate of the speed of that decay
(see [ebisu](https://fasiha.github.io/post/ebisu/)).

At any time, you can inspect the 'Bayesian status' of your deck with the
command `mg status`. You will see a histogram of the expected probability of
recall at that moment according to the Bayesian memory model's estimates
of the half-life of your memory for each card.

```
$ mg status
** welcome **
probability of recall histogram:
[  0%,   5%] (0)
(  5%,  10%] (0)
( 10%,  15%] (0)
( 15%,  20%] (0)
( 20%,  25%] (0)
( 25%,  30%] (0)
( 30%,  35%] (0)
( 35%,  40%] (0)
( 40%,  45%] (0)
( 45%,  50%] (0)
( 50%,  55%] (0)
( 55%,  60%] (0)
( 60%,  65%] (0)
( 65%,  70%] (0)
( 70%,  75%] (0)
( 75%,  80%] (0)
( 80%,  85%] (0)
( 85%,  90%] (0)
( 90%,  95%] (0)
( 95%, 100%] (6) ████████████████████████████████████████████████████████
6 cards seen (60%), 4 cards unseen (40%)
```

Initially, of course, all of the cards will have been recently reviewed,
and so with a high probability of recall (low probability of forgetting).
But if you try again after some time, some of the memories will be
predicted to have decayed, at a rate depending on how to rated them in
the learning session:

```
$ mg status
** welcome **
probability of recall histogram:
[  0%,   5%] (0)
(  5%,  10%] (0)
( 10%,  15%] (0)
( 15%,  20%] (0)
( 20%,  25%] (2) █████████████████████████████████████▍
( 25%,  30%] (0)
( 30%,  35%] (0)
( 35%,  40%] (0)
( 40%,  45%] (0)
( 45%,  50%] (0)
( 50%,  55%] (0)
( 55%,  60%] (0)
( 60%,  65%] (0)
( 65%,  70%] (0)
( 70%,  75%] (0)
( 75%,  80%] (0)
( 80%,  85%] (0)
( 85%,  90%] (0)
( 90%,  95%] (1) ██████████████████▊
( 95%, 100%] (3) ████████████████████████████████████████████████████████
6 cards seen (60%), 4 cards unseen (40%)
```

Finally, you can get a more detailed breakdown of the per-card probabilities
with some of the other options from the status mode, such as the `--list`
option:

```
$ mg status --list
** welcome **
cards (probability of recall):
   1. 4--vier [191s ago]                                              ( 23.9%)
   2. 5--fünf [180s ago]                                              ( 25.0%)
   3. 1--eins [193s ago]                                              ( 94.9%)
   4. 3--drei [183s ago]                                              ( 95.2%)
   5. 2--zwei [195s ago]                                              ( 99.9%)
   6. 0--null [186s ago]                                              ( 99.9%)
   7. 6--sechs                                                        (unseen)
   8. 7--sieben                                                       (unseen)
   9. 8--acht                                                         (unseen)
  10. 9--neun                                                         (unseen)
```

Watch out for spoilers! Your reading the solutions on these cards will not be
taken into account in the time-since-last-review when you next drill these
cards.

## Step 4: Drill a deck

Now for the main event: To practice our flashcards with with `mg`!
For this, we use 'drill' mode, `mg drill`.
Simply run:

```
$ mg drill
```

`mg` will use the memory model to find the six (see `--num_cards` flag to
change the length of the session) most-likely-to-be-forgotten flashcards
and shuffle these into a drill session for you.
We only have six cards learned so far, so they'll all appear in this first
session. You'll see something like this:

```
** welcome **
drill some old cards...
** drill 1/6 **
prompt: 5
recall: 
```

The first flashcard's prompt is '5', and 'recall:' is instructing you to
type your guess as to the back of the card. Let's go ahead and put in the
correct answer. Can you recall it?

```
recall: fünf
answer: fünf
```

We entered the right answer, as confirmed by the 'answer' response.
This happened to be one of the cards which the memory model thought
we would likely get wrong, so it will update that belief and adjust
the estimate of the half-life, causing the memory to decay slower
next time.

What's next?

```
** drill 2/6 **
prompt: 3
recall:
```

The next card is '3'. Just to see what happens, let's forget that the
answer is 'drei' and enter something incorrect:

```
recall: zwei
answer: drei
commit:                                 forgot (↵) | got it (g+↵) | skip (s+↵)
```

`mg` informs us that this is not correct, and asks us for confirmation.
Did we really mean to type 'zwei' ('forgot', enter), or was this some kind
of typo and we actually knew it ('got it', g+enter)? Or was there some other
reason why we should invalidate this question and forgo updating the memory
model ('skip', s+enter).

We meant to type 'zwei', so admit that we forgot the answer by pressing
enter.

Next?

```
** drill 3/6 **
prompt: 2
recall:
```

Okay. This one is definitely 'zwei'!

```
recall: zwei'
answer: zwei
commit: g                               forgot (↵) | got it (g+↵) | skip (s+↵)
got it!
```

Oops! I accidentally hit the ' key before pressing enter, and so the strings
didn't match. But I didn't forget the answer, so this time I overrode the
comparison by pressing 'g' and enter.


Anyway, that's the basic mechanics of drilling flashcards with `mg`.
Some final notes:

* Continue until the end of the session for the model to be saved to disk.
* If you need to or want to abort the session early, you can send
  '^C' (control+C) (the session so far will be saved) or
  '^D' (control+D) (the session so far will not be saved).
* You can also drill cards *backwards*, that is, to type the front of the
  card after being prompted with the back of the card. Use the `--reverse`
  flag for this.

## Step 5: Customising nodes

There are several additional optional features which can enhance the
flexibility of deck creation. 

### Terminology: Nodes, Links, Knowledge Graph

First a note on terminology. The deck generation script and its main
function are called 'graph' because the tuples are termed the 'links'
of a 'knowledge graph'. Likewise, each of their two components is a
'node'.
This is a more general notion than 'flashcard deck', 'flashcard',
'side', and it's the terminology we'll continue with when discussing
further customisation options below.

### Topics

The most basic enhancement is to add 'topics' to each link. This can later
be used to filter for certain subgroups of cards for when the collection of
decks and cards in the current directory is much larger.
(see `mg drill --help` for information on how to specify topics).
Specifying topics for a knowledge link requires adding a dot-separated string
of topics as a third component to the link tuple in the generator function.
For example, we could add the topics `de` and `digits` to all ten cards in
our deck as follows:

```python
D = ['null','eins','zwei','drei','vier','fünf','sechs','sieben','acht','neun']
def graph():
    for i, n in enumerate(D):
        yield i, n, "de.digits"
# +               ^^^^^^^^^^^^^
```

TODO: UPDATED UP TO HERE
TODO: ADD FILENAME TO TOPICS


### Custom display and comparison strings

We might want to separate the strings we use for prompting from the
strings we use for checking typed answers against, and we might want
both of these to be different from the strings we use for indexing
the memory model (see [Step 6](#step-6-modifying-a-deck-after-learning)
below for more on indexing).

I don't see any of these options as super useful in the case of our
example, but in some other cases (such as when drilling German nouns
separately from their genders, but still wanting to note the gender
when displaying the answer) it can be very useful.

To do it, replace the first two components of the tuples in the graph
generator function with objects of type `mg.graph.Node`, which
optionally takes these three separate types of string as constructor
arguments:

```python
from mg.graph import Node
# ^^^^^^^^^^^^^^^^^^^^^^^

D = ['null','eins','zwei','drei','vier','fünf','sechs','sieben','acht','neun']
def graph():
    for i, n in enumerate(D):
        yield (
            Node(i, print_str=format(i, "06d"), match_str=i),
            Node(n, print_str=format(n, ">6s"), match_str=n),
#           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        )
```

For no particular reason, this example demonstrates formatting the digits
and their translations as six characters wide in prompts and displayed
answers (`print_str=`). The string used the indexing (the positional
argument of the constructor) and answer-comparison (`match_str=`) are
unchanged. The result:

```
prompt: 000003
recall: drei
answer:   drei
```

In the future, it will be possible to specify custom answer-comparison
functions, for example so as to allow case-insensitive matching or to
perform other normalisation where appropriate.

### Text-to-Speech

By installing the optional utility
[`espeak`](https://github.com/espeak-ng/espeak-ng/)
on your system,
you will enable Text-to-Speech functionality in `mg`---to read out the
prompts and correct answers to you as you practice!
However, even with `espeak` installed, you have to tell `mg` that your
nodes are to be spoken, and in which language. The same `mg.graph.Node`
class is used for this, with the constructor arguments `speak_str` and
`speak_voice`.

For example, the following script has number prompts spoken in English
(`espeak` voice `en`) and answers spoken in German (voice `de`). See
`espeak`'s documentation for a list of voices.

```python
from mg.graph import Node
# ^^^^^^^^^^^^^^^^^^^^^^^

D = ['null','eins','zwei','drei','vier','fünf','sechs','sieben','acht','neun']
def graph():
    for i, n in enumerate(D):
        yield (
            Node(i, speak_str=i, speak_voice="en"),
            Node(n, speak_str=n, speak_voice="de"),
#           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        )
```

### Duplicate nodes

Sometimes it will be necessary to have multiple nodes (front or back of
cards) in the same graph (deck) with the same value (specifically, the
same index string).
`mg` can handle this fine, so you don't need to go out of your way to
uniquely index your cards.
If multiple cards would have the same index string
(TODO: should it be *same print string*?)
`mg` will add a unique number (1, 2, ...) to the print string, so that
you can learn which answer to give along with which version of the prompt.

## Step 6: Modifying a deck after learning

The memory model parameters are stored in the deck directory in a JSON
file called `data.json` (in our example, that's `de.digits.mg/data.json`).
Within are the parameters for each card, keyed by a string made up of the
card's front and back 'index strings'
(see [above](#custom-display-and-comparison-strings))
and, if present, the optional topic (see [above](#topics)).

The advantage of this is that you can reorder/insert into the generator
script's output as much as you like and they will still be found.

But the disadvantage is that if you change the value or even the spelling
of a node, its index into the data file will change, and the memory
parameters already there will be orphaned.

Sometimes, for example when you are simply correcting a card, you want
to keep the same parameters. In this case, unfortunately, the only
way to achieve this is to go into `data.json`, find the entry with the
old key, and update the key (ensuring no current `mg` sessions later
save over your modifications, such as at the end of a learning or
drill session).

In other cases, you want to reset the parameters, as if you were deleting
the old card and creating a new one. Then you can either leave the
orphaned entry in the data file (it does no harm other than taking up
space) or you can find and delete it manually.

> #### Help Wanted:
> 
> Unfortunately this step is quite clunky.
> I'm still thinking about the best way to handle this process
> of maintaining these data file references.
> Do you have any ideas? Let me know!
