import itertools

from mg.io import print
from mg.color import colormap_red_green, to_hex


def print_hist(data, lo=None, hi=None, bins=30, height=22,
        labelformat="4.2f", countformat="", color=colormap_red_green):
    """
    Print a histogram plot of the sequence of samples in `data`, binned
    into  boundaries `bins` (if `bins` is an int, then the data are
    separated into `bins` even width bins between `lo` (default: min(data)
    and `hi` (default: max(data)).

    The bin boundaries are shown below each bin using `labelformat` and
    the counts are shown with `countformat`. The bars are colored using
    the colormap `color`. TODO: Allow single color.
    """
    data = list(data)
    # decide boundaries and bins
    if isinstance(bins, int):
        nbins = bins
        if lo is None: lo = min(data)
        if hi is None: hi = max(data)
        bins = [lo + i/nbins * (hi - lo) for i in range(nbins+1)]
    else:
        nbins = len(bins) - 1
        lo = bins[0]
        hi = bins[-1]
    # build their labels
    labels = []
    for i, (b1, b2) in enumerate(zip(bins, bins[1:])):
        l1 = format(b1, labelformat)
        l2 = format(b2, labelformat)
        lb = "(" if i else "["
        labels.append(f"{lb}{l1}, {l2}]")
    # count data points in each bin
    cumuls = [sum(d <= b for d in data) for b in bins]
    cumuls[0]  = 0 # shift anything on low boundary into low bucket
    counts = [cumuls[i] - cumuls[i-1] for i in range(1, nbins+1)]
    # decide the colours
    colors = [to_hex(color((b2 - lo) / (hi - lo))) for b2 in bins[1:]]
    # plot the graph (a bar chart)
    print_bars(
            values=counts,
            labels=labels,
            colors=colors,
            height=height,
            valueformat=countformat,
            labelformat="",
        )


def print_bars(values, labels=None, colors=None, height=22,
        valueformat="", labelformat=""):
    """
    Print a bar chart with `values` and options below `labels`. `colors`
    is an optional list of `colors` of the bars. The values are printed
    below each bar with format `valueformat` and the labels are formatted
    with `labelformat`.
    """
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
    """
    Return a character representing a partly-filled cell with proportion
    `f` (rounded down to width of nearest available character).
    """
    return [" ", "▏", "▎", "▍", "▌", "▋", "▊", "▉", "█"][int(9*f)]
