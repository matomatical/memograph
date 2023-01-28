from mg.mgio import print, input
from mg.plot import print_hist
from mg.color import colormap_red_green as color, to_hex

def run_status(graph, options):
    if options.histogram:
        plot_histogram(graph, options.topics)
    if options.posterior:
        plot_posterior(graph, options.topics)
    if options.scatter:
        plot_scatter(graph, options.topics)
    if options.list:
        plot_list(graph, options.topics)


def plot_histogram(graph, topics):
    n_seen  = graph.count(topics=topics, new=False)
    n_new   = graph.count(topics=topics, new=True)
    n_total = n_seen + n_new
    if n_total == 0:
        print("no cards! try adding some or changing the topic.")
        return
    if n_seen > 0:
        print("probability of recall histogram:")
        probs = [l.m.predict(exact=True) for l in graph.query(topics=topics)]
        print_hist(probs, lo=0, hi=1, bins=20, height=56, labelformat="4.0%")
    print(
        f"{n_seen} cards seen ({n_seen/n_total:.0%}),",
        f"{n_new} cards unseen ({n_new/n_total:.0%})"
    )


# TODO
def plot_posterior(graph, topics):
    print("posterior plot: not yet implemented.")


# TODO
def plot_scatter(graph, topics):
    print("scatter plot: not yet implemented.")


def plot_list(graph, topics):
    print("cards (probability of recall):")
    i = 1
    for link in graph.query(topics=topics, new=False):
        p = link.m.predict(exact=True)
        c = to_hex(color(p))
        print(f"<bold>{i:>4d}.<reset>", link, r=f"(<{c}>{p:>6.1%}<reset>)")
        i += 1
    for link in graph.query(topics=topics, new=True):
        print(f"<bold>{i:>4d}.<reset>", link, r="(<faint>unseen<reset>)")
        i += 1

