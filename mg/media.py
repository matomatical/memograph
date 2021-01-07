import sys
import queue
import threading
from subprocess import run, DEVNULL

class MediaDaemon:
    def __init__(self):
        self.error = False
        self.queue = queue.SimpleQueue()
        self.thread = threading.Thread(target=self.loop, daemon=True)
        self.thread.start()
    def loop(self):
        while not self.error:
            args = self.queue.get()
            try:
                run(args, stdout=DEVNULL, stderr=DEVNULL)
            except FileNotFoundError as e:
                print(
                        "\nError: TTS command failed with",
                        e,
                        "(did you install `espeak` command?).",
                        "Disabling TTS, but you can continue the session.",
                        file=sys.stderr
                    )
                self.error = True
    def schedule(self, *args):
        self.queue.put(args)

md = MediaDaemon()

def speak(text, voice="english"):
    """
    Speak some text with a given voice. Uses `espeak` library.
    The default voice is "english", but you can use any VoiceName
    (see `espeak --voices`).

    TODO: Allow other kwargs, passed to espeak command.
    TODO: Allow configuration of the TTS engine (e.g. allow 'say' on macos).
    """
    md.schedule("espeak", text, "-v", voice)
