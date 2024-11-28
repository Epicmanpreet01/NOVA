import multiprocessing

#run the application
def StartNova():
    print("Nova launching")
    from main import start
    start()

#run wake word detection

def listenWakeWord():
    print("HotWord recognizing")
    from engine.wakeWordService import WakeWordService
    service = WakeWordService()
    service.run()


#uses multiprocessing to run both the commands simultanously side-by-side
if __name__ == "__main__":
    p1 = multiprocessing.Process(target = StartNova)
    p2 = multiprocessing.Process(target = listenWakeWord)
    p1.start()
    p2.start()
    p1.join()

    if p2.is_alive():
        p2.terminate()
        p2.join()
    
    print("system stop")