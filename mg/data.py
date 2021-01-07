"""
utility functions for parsing lists of links
"""

def parse(links_text, sep="--", skip_header=True):
    for line in links_text.splitlines()[skip_header:]:
        if sep not in line:
            continue
        # remove comments, whitespace
        line = line.split("#", maxsplit=1)[0].strip()
        fields = tuple(map(str.strip, line.split(sep)))
        if fields[0] == "":
            fields = prefix + fields[1:]
        if fields[-1] == "":
            prefix = fields[:-1]
        else:
            yield fields
