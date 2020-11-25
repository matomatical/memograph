import math

def graph():
    for n in range(10+1):
        yield (
                "math.factorial",
                f"${n}!$",
                f"${math.factorial(n)}$"
            )
