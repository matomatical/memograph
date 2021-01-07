from mg.graph import Node

D = ['null','eins','zwei','drei','vier','fünf','sechs','sieben','acht','neun']
def graph():
    for i, n in enumerate(D):
        yield (
            Node(i, speak_str=i, speak_voice="en"),
            Node(n, speak_str=n, speak_voice="de"),
        )
