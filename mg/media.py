import queue
import threading
from subprocess import run, DEVNULL

class MediaDaemon:
    def __init__(self):
        self.queue = queue.SimpleQueue()
        self.thread = threading.Thread(target=self.loop, daemon=True)
        self.thread.start()
    def loop(self):
        while True:
            args = self.queue.get()
            run(args, stdout=DEVNULL, stderr=DEVNULL)
    def schedule(self, *args):
        self.queue.put(args)

md = MediaDaemon()

def speak(text, voice="english"):
    """
    Speak some text with a given voice. Uses `espeak` library.
    The default voice is "english", but you can use any VoiceName
    (see `espeak --voices`).

    TODO: Allow other kwargs, passed to espeak command.
    """
    md.schedule("espeak", text, "-v", voice)
