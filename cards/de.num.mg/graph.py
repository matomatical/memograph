D = ['null','ein','zwei','drei','vier','fünf','sechs','sieben','acht','neun']

def graph():
    ns = [
        simplify(
            # f"{d0}hundert"
            # f"{d2}"
            # f"und{d1}zigtausend"
            # f"{d3}hundert"
            f"{d5}"
            f"und{d4}zig"
        )
        # for d0 in D
        # for d1 in D
        # for d2 in D
        # for d3 in D
        for d4 in D
        for d5 in D
    ]
    return (("de.num.99", i, n) for i, n in enumerate(ns))


def simplify(n):
    n = n.replace("undnullzig", "")
    n = n.replace("nullzig", "")
    n = n.replace("nullund", "")
    # teens
    n = n.replace("einzig", "zehn")
    n = n.replace("undzehn", "zehn")
    n = n.replace("einzehn", "elf")
    n = n.replace("sechszehn", "sechzehn")
    n = n.replace("siebenzehn", "siebzehn")
    # tens
    n = n.replace("zweizig", "zwanzig")
    n = n.replace("dreizig", "dreißig")
    n = n.replace("zweizehn", "zwölf")
    n = n.replace("sechszig", "sechzig")
    n = n.replace("siebenzig", "siebzig")
    # hundreds and thousands
    n = n.replace("nullhundert", "")
    n = n.replace("hundertnull", "hundert")
    n = n.replace("nulltausend", "")
    n = n.replace("tausendnull", "tausend")
    if n == "ein": n = "eins"
    return n

