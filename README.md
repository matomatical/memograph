# memograph

A utility for drilling flashcards based on an online Bayesian
spaced-repetition memory model^[1].

## Installation

* Install Python 3.7 or higher.
* Clone this repository and cd into this dirctory.
* Install requirements `ebisu` and `prompt_toolkit`,
  e.g. with `pip install -r requirements.txt`.
* Delete all deck progress files (they contain *my* memory model parameters),
  e.g. with `rm cards/*/data.json`.

## Usage


## Deck format

You can create your own 

## TODO list

* Switch to `prompt_toolkit` for the UI/response entry, including colours,
  and better keyboard controls.
* Add multimedia extensions:
  * Sound effects
  * Text-to-speech e.g. for language cards
  * Mathematics equations (in the terminal?!)
  * Support image-based flashcards.
* Find a nice way to allow custom assessment.
* Implement 'Bayesian deck status' command to show a snapshot of memory for
  a whole deck (maybe including my own implementation of `termplotlib`).

Eventually, long-term project goals:
* Separate deck progress from repo so that users don't have to delete them.
* Reimplement `ebisu` (for fun and either vectorisation or no numpy).
* Perhaps switch to a domain-specific language for specifying the graphs.
* Switch to a richer, 

^[1]: [ebisu](https://github.com/fasiha/ebisu)

