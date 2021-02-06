from mg.io import print, input
from mg.plot import print_bars
from mg.color import colormap_red_green as color, to_hex

def run_info(graph, options):
    keys = list(filter_topics(options.topics, graph))
    # to many cards
    if len(keys) > 1:
        print(f"multiple ({len(keys)}) matches:") 
        for i, key in enumerate(keys, 1):
            print(f"<bold>{i:4d}.<reset> {key}")
    
    # not enough cards
    elif len(keys) < 1:
        print("<bold><red>no matches!<reset> try again") 

    # just right!
    else:
        key = keys[0]
        link = list(graph.links[key])[0]
        print(f"<bold><green>match!<reset> {key}")
        print("topics:", link.t)
        print("node 1:", link.u.label())
        print("node 2:", link.v.label())
        if link.m.is_new():
            print("status: not yet learned")
        else:
            print("status: last reviewed", link.m.elapsed(), "seconds ago")
            print("params:", link.m)
            print("recall:")
            # pdf histogram # TODO: use CDF instead duh
            support = [(p+0.5)/20 for p in range(20)]
            pdf = [link.m.density(p)/20 for p in support]
            print_bars(
                values=pdf,
                labels=support,
                labelformat=".1%",
                valueformat=".3f",
                colors=[to_hex(color(p)) for p in support],
            )


def filter_topics(topics, graph):
    for key in graph.keys:
        if all(t in key for t in topics):
            yield key
