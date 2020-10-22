import os
import threading

import playsound

_SOUNDS = {
    'heart': 'mg/audio/heart.mp3',
    'streak': 'mg/audio/streak.mp3',
    'right': 'mg/audio/right.mp3',
    'wrong': 'mg/audio/wrong.mp3',
}

def sound(name):
    path = _SOUNDS[name]
    thread = threading.Thread(
        target=playsound.playsound,
        args=(path,),
        kwargs={'block': True},
        daemon=False,
    )
    thread.start()
