from mg.graph import Link

deck = [
    Link(
        "alpha.chr--aid.a--z",
        chr(i+ord('a')),
        str(i+1),
    )
    for i in range(26)
]
