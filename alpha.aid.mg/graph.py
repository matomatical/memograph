
def graph():
    for i in range(26):
        yield ("alpha.aid", chr(i+ord('a')), str(i+1))
