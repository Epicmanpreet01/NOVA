import struct
import pvporcupine
import pyaudio
import logging
import os
import eel
from engine.config import PICOVOICE_ACCESS_KEY
from time import sleep


class WakeWordService:
    def __init__(self):
        self.running = True
        self.porcupine = None
        self.audio = None
        self.stream = None

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            filename="wake_word.log"
        )

        self.keyword_path = os.path.join(
            os.path.dirname(__file__),
            "wakeWord",
            "Nova-open_en_windows_v3_0_0.ppn"
        )
        
    def start(self):
        try:
            self.porcupine = pvporcupine.create(
                access_key=PICOVOICE_ACCESS_KEY,
                keywords=["jarvis"],
                sensitivities=[0.7]
            )

            self.audio = pyaudio.PyAudio()
            self.stream = self.audio.open(
                rate=self.porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.porcupine.frame_length
            )

            print("Wake word listening... (say 'Jarvis')")

            while self.running:
                pcm = self.stream.read(
                    self.porcupine.frame_length,
                    exception_on_overflow=False
                )

                pcm = struct.unpack_from(
                    "h" * self.porcupine.frame_length,
                    pcm
                )

                if self.porcupine.process(pcm) >= 0:
                    print("Wake word detected")
                    eel.triggerAssistant()
                    sleep(2)

        except Exception as e:
            print(f"Wake word error: {e}")

        finally:
            self.cleanup()

    def on_detected(self):
        print("Wake word detected")
        eel.triggerAssistant()

    def stop(self):
        self.running = False

    def cleanup(self):
        if self.stream:
            self.stream.close()
        if self.audio:
            self.audio.terminate()
        if self.porcupine:
            self.porcupine.delete()
        logging.info("Wake word service stopped")
