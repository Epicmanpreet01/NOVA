import numpy as np
import sounddevice as sd
from engine.audio_engine.models import kokoro_pipeline


def tts_kokoro_blocking(text: str):
    generator = kokoro_pipeline(
        text,
        voice="af_heart",
        speed=1
    )

    audio = np.concatenate([a for _, _, a in generator])

    silence = np.zeros(int(24000 * 0.4), dtype=np.float32)
    audio = np.concatenate([silence, audio, silence])

    sd.play(audio, samplerate=24000)
    sd.wait()
