from engine.functionality import *
from engine.onCommand import *
from engine.wakeWordService import WakeWordService

import os
import eel
import threading


def start():
    eel.init("static")
    wake_service = WakeWordService()
    wake_thread = threading.Thread(
        target=wake_service.start,
        daemon=True
    )
    wake_thread.start()
    print("Wake word listening...")
    playSound()

    os.system('start chrome.exe --app="http://localhost:8000/index.html"')

    eel.start(
        'index.html',
        mode=None,
        host='localhost',
        block=True
    )


if __name__ == "__main__":
    start()
