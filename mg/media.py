from subprocess import Popen, DEVNULL

def _background(*argv):
    """
    Run a process in the background (detach and immediately return)
    """
    Popen(argv, stdout=DEVNULL, stderr=DEVNULL)


def sound(path):
    """
    Play a sound at a given data path
    """
    _background("ffplay", "-nodisp", "-autoexit", path)


def speak(text, voice="english"):
    """
    Speak some text with a given voice. Uses `espeak` library.
    The default voice is "english", but you can use any VoiceName
    (see `espeak --voices`).

    TODO: Allow other kwargs, passed to espeak command.
    """
    _background("espeak", text, "-v", voice)
