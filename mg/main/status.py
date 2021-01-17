from mg.io import print, input
from mg.plot import print_hist
from mg.color import colormap_red_green as color, to_hex

def run_status(deck, options):
    # check at least one selected
    ps = [
            options.histogram,
            options.posterior,
            options.scatter,
            options.list
        ]
    if not any(ps):
        options.histogram = True

    # plot!
    if options.histogram:
        plot_histogram(deck)
    if options.posterior:
        plot_posterior(deck)
    if options.scatter:
        plot_scatter(deck)
    if options.list:
        plot_list(deck)


def plot_histogram(deck):
    n_seen  = deck.num_old()
    n_new   = deck.num_new()
    n_total = n_seen + n_new
    if n_total == 0:
        print("no cards! try adding some or changing the topic.")
        return
    if n_seen:
        print("probability of recall histogram:")
        probs = [c.predict(exact=True) for c in deck.draw()]
        print_hist(probs, lo=0, hi=1, bins=20, height=56, labelformat="4.0%")
    print(
        f"{n_seen} cards seen ({n_seen/n_total:.0%}),",
        f"{n_new} cards unseen ({n_new/n_total:.0%})"
    )


# TODO
def plot_posterior(deck):
    print("posterior plot: not yet implemented.")


# TODO
def plot_scatter(deck):
    print("scatter plot: not yet implemented.")


def plot_list(deck):
    print("cards (probability of recall):")
    i = 1
    for card in deck.draw():
        p = card.predict(exact=True)
        c = to_hex(color(p))
        print(f"<bold>{i:>4d}.<reset>", card, r=f"(<{c}>{p:>6.1%}<reset>)")
        i += 1
    for card in deck.draw_new():
        print(f"<bold>{i:>4d}.<reset>", card, r="(<faint>unseen<reset>)")
        i += 1

