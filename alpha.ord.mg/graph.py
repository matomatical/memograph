from mg.graph import Link

def graph():
    for i in range(ord('a'), ord('z')+1):
        yield ("alpha.ord.lower", chr(i), str(i))
    for i in range(ord('A'), ord('Z')+1):
        yield ("alpha.ord.upper", chr(i), str(i))
