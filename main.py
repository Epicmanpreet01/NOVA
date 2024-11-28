from engine.functionality import *
from engine.onCommand import *
import os
import eel
from multiprocessing import shared_memory
import threading
import time

def check_wake_word():
    try:
        shm = shared_memory.SharedMemory(name='wake_word_trigger')
        while True:
            if shm.buf[0] == 1:
                # Reset the trigger
                shm.buf[0] = 0
                # Trigger the voice assistant
                eel.triggerAssistant()
            time.sleep(0.1)  # Small sleep to prevent CPU hogging
    except Exception as e:
        print(f"Wake word checker error: {e}")
    finally:
        if shm is not None:
            shm.close()

def start():
    eel.init("static")
    
    # Start wake word checker in a separate thread
    wake_word_thread = threading.Thread(target=check_wake_word, daemon=True)
    wake_word_thread.start()
    
    playSound()
    
    os.system('start chrome.exe --app="http://localhost:8000/index.html"')
    eel.start('index.html', mode=None, host='localhost', block=True)