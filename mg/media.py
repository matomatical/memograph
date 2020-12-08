try:
    import espeakng
    speaker = espeakng.Speaker()
    def speak(text, voice="en"):
        speaker.voice = voice
        speaker.say(text, wait4prev=True)
except:
    import sys
    def speak(text, voice="en"):
        print("warning: loading espeak-NG failed", file=sys.stderr)
