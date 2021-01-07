import sys
import queue
import threading
from subprocess import run, DEVNULL

class MediaDaemon:
    def __init__(self):
        self.queue = queue.SimpleQueue()
        self.thread = threading.Thread(target=self.loop, daemon=True)
        self.thread.start()
    def loop(self):
        try:
            while True:
                args = self.queue.get()
                result = run(args, capture_output=True, text=True)
                if result.returncode != 0:
                    raise Exception(
                            f"Exit with non-zero return code "
                            f"{result.returncode} and stderr: "
                            f"{result.stderr.strip()}"
                        )
        except Exception as e:
            print(
                "\nERROR Media command failed:\n",
                e,
                "\n(did you install media engines to your path?)."
                "\nDisabling media for this session, but you can continue.",
                file=sys.stderr,
            )
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
