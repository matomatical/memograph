import math
from mg.graph import Link, MathNode

deck = [
    Link(
        "math.factorial.0--10",
        MathNode(f"{n}!"),
        MathNode(f"{math.factorial(n)}"),
    )
    for n in range(10+1)
]
