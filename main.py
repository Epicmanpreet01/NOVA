from engine.functionality import *
from engine.onCommand import *
from engine.wakeWordService import WakeWordService

import os
import eel
import threading

import queue

_ui_queue = queue.Queue()

def _ui_loop():
    while True:
        fn = _ui_queue.get()
        try:
            fn()
        except Exception as e:
            print("UI error:", e)

threading.Thread(target=_ui_loop, daemon=True).start()

def trigger_ui():
    _ui_queue.put(lambda: eel.triggerAssistant())


def start():
    eel.init("static")
    wake_service = WakeWordService(on_detected=trigger_ui)
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
