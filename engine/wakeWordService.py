import struct
import pvporcupine
import pyaudio
import logging
import json
import os
from multiprocessing import shared_memory
import numpy as np
from time import sleep

class WakeWordService:
    def __init__(self):
        self.porcupine = None
        self.audio = None
        self.audio_stream = None
        self.is_running = True
        
        # Setup shared memory for inter-process communication
        try:
            self.shm = shared_memory.SharedMemory(name='wake_word_trigger', create=True, size=1)
        except FileExistsError:
            self.shm = shared_memory.SharedMemory(name='wake_word_trigger')
        
        # Initialize shared memory with 0
        self.shm.buf[0] = 0
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='wake_word.log'
        )
        
    def initialize(self):
        try:
            self.porcupine = pvporcupine.create(keywords=["jarvis", "alexa", "computer"])
            self.audio = pyaudio.PyAudio()
            self.audio_stream = self.audio.open(
                rate=self.porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.porcupine.frame_length
            )
            logging.info("Wake word service initialized successfully")
            return True
            
        except Exception as e:
            logging.error(f"Failed to initialize wake word service: {str(e)}")
            self.cleanup()
            return False
    
    def run(self):
        if not self.initialize():
            return
        
        logging.info("Wake word service started")
        
        try:
            while self.is_running:
                audio_frame = self.audio_stream.read(self.porcupine.frame_length)
                audio_frame = struct.unpack_from("h" * self.porcupine.frame_length, audio_frame)
                
                keyword_index = self.porcupine.process(audio_frame)
                
                if keyword_index >= 0:
                    logging.info("Wake word detected")
                    self.trigger_action()
                    # Wait a bit to prevent multiple triggers
                    sleep(2)
                    
        except Exception as e:
            logging.error(f"Error in wake word service: {str(e)}")
        finally:
            self.cleanup()
    
    def trigger_action(self):
        try:
            # Set shared memory flag to 1 to indicate wake word detected
            self.shm.buf[0] = 1
            logging.info("Wake word trigger set")
        except Exception as e:
            logging.error(f"Failed to trigger action: {str(e)}")
    
    def cleanup(self):
        if self.audio_stream is not None:
            self.audio_stream.close()
        
        if self.audio is not None:
            self.audio.terminate()
            
        if self.porcupine is not None:
            self.porcupine.delete()
            
        self.shm.close()
        if self.is_running:  # Only unlink if we're the creator
            try:
                self.shm.unlink()
            except Exception:
                pass
        
        logging.info("Wake word service cleaned up")
    
    def stop(self):
        self.is_running = False
        logging.info("Wake word service stop requested")

if __name__ == "__main__":
    service = WakeWordService()
    service.run()