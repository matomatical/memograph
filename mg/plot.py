from mg.io import print
from mg.color import colormap_red_green as color

def print_hist(data, lo=0, hi=1, width=50, height=22, labelformat="4.2f"):
    data = list(data)

    bins = [lo + i/width * (hi - lo) for i in range(width+1)]
    cumuls = [sum(d <= b for d in data) for b in bins]
    cumuls[0] = 0
    counts = [cumuls[i] - cumuls[i-1] for i in range(1, width+1)]
    cmax = max(counts)
    heights = [height * c / cmax for c in counts]

    for i, (b1, b2, h) in enumerate(zip(bins, bins[1:], heights)):
        l1 = format(b1, labelformat)
        l2 = format(b2, labelformat)
        bar = int(h) * "█" + _part(h - int(h))
        lob = "(" if i else "["
        col = color(b2)
        print(f"{lob}{l1}, {l2}]", f"<style fg='{col}'>{bar}</style>")


def _part(f):
    i = int(9*f)
    return [" ", "▏", "▎", "▍", "▌", "▋", "▊", "▉", "█"][i]
