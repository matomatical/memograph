def graph():
    for n in range(20+1):
        for m in range(n+1):
            yield (
                    "math.tables",
                    f"${n} \\times {m}$"),
                    f"${n*m}$"
                )
