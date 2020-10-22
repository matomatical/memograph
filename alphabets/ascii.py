from mg.graph import Link

deck = [
    Link(
        "alpha.chr--ord.a--z",
        chr(i),
        str(i),
    )
    for i in range(ord('a'), ord('z')+1)
]
