"""
utility functions for parsing lists of links
"""

def parse(links_text, sep="--", skip_header=True):
    for line in links_text.splitlines()[skip_header:]:
        if sep not in line:
            continue
        yield tuple(map(str.strip, line.split("#")[0].split(sep)))
