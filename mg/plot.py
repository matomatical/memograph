import itertools

from mg.io import print
from mg.color import colormap_red_green as color, to_hex

def print_hist(data, lo=0, hi=1, width=50, height=22, labelformat="4.2f"):
    data = list(data)
    C = len(str(len(data)))
    bins = [lo + i/width * (hi - lo) for i in range(width+1)]
    cumuls = [sum(d <= b for d in data) for b in bins]
    cumuls[0] = 0
    counts = [cumuls[i] - cumuls[i-1] for i in range(1, width+1)]
    cmax = max(counts)
    heights = [height * c / cmax for c in counts]

    for i, (b1, b2, c, h) in enumerate(zip(bins, bins[1:], counts, heights)):
        l1 = format(b1, labelformat)
        l2 = format(b2, labelformat)
        l3 = format(c, f">{C}d")
        bar = int(h) * "█" + _part(h - int(h))
        lob = "(" if i else "["
        col = to_hex(color(b2))
        print(f"{lob}{l1}, {l2}] ({l3})", f"<{col}>{bar}<reset>")


def print_bars(values, labels=None, colors=None, width=50, height=22,
        valueformat="", labelformat=""):
    values = list(values)
    if colors is None: colors = itertools.repeat("#22dd22")
    # compute the bar heights
    vmax = max(values)
    heights = [height * v / vmax for v in values]
    # balance the labels and valuelabels
    if labels is not None:
        labels = [format(l, labelformat) for l in labels]
        lmax = max(len(l) for l in labels)
        labels = [l.rjust(lmax)+" " for l in labels]
    else:
        labels = itertools.repeat("")
    valuelabels = [format(v, valueformat) for v in values]
    vlmax = max(len(vl) for vl in valuelabels)
    valuelabels = [f"({vl.rjust(vlmax)}) " for vl in valuelabels]
    
    # print the bars
    for lab, vlab, ht, col in zip(labels, valuelabels, heights, colors):
        bar = int(ht) * "█" + _part(ht - int(ht))
        print(lab, vlab, f"<{col}>{bar}<reset>", sep="")


def _part(f):
    return [" ", "▏", "▎", "▍", "▌", "▋", "▊", "▉", "█"][int(9*f)]
