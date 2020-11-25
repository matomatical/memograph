import codecs

def graph():
    for i in range(ord('a'), ord('z')+1):
        yield ("alpha.rot13", chr(i), codecs.encode(chr(i), 'rot13'))
