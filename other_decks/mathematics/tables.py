from mg.graph import Link, MathNode

deck = [
    Link(
        "math.tables.1--20x1--20",
        MathNode(f"{n} \\times {m}"),
        MathNode(f"{n*m}"),
    )
    for n in range(1, 20+1)
    for m in range(1, 20+1)
]
