import codecs
from mg.graph import Link

deck = [
    Link(
        "alpha.rot13.lower",
        chr(i),
        codecs.encode(chr(i), 'rot13'),
    )
    for i in range(ord('a'), ord('z')+1)
]
