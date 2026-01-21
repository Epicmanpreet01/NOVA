import sounddevice as sd
import numpy as np
import queue
import torch

from engine.audio_engine.models import (
    whisper_processor,
    whisper_model,
    device,
)

SAMPLERATE = 16000
CHANNELS = 1
BLOCKSIZE = 1024
TARGET_SECONDS = 3.5
OVERLAP = 0.75

SILENCE_THRESHOLD = 0.005
MAX_SILENCE_SECONDS = 3.0

_audio_queue = queue.Queue(maxsize=50)


def _rms(audio):
    return np.sqrt(np.mean(audio ** 2))


def _normalize(audio):
    rms = np.sqrt(np.mean(audio ** 2))
    return audio / (rms + 1e-6)


def _audio_callback(indata, frames, time_info, status):
    try:
        _audio_queue.put_nowait(indata[:, 0].astype(np.float32))
    except queue.Full:
        pass


def _collector():
    buffer = np.zeros(0, dtype=np.float32)
    target_len = int(TARGET_SECONDS * SAMPLERATE)
    overlap_len = int(OVERLAP * SAMPLERATE)

    while True:
        chunk = _audio_queue.get()
        buffer = np.concatenate([buffer, chunk])

        if len(buffer) >= target_len:
            yield buffer[:target_len]
            buffer = buffer[target_len - overlap_len:]


def listen_once_whisper() -> str:
    transcript = []
    silence_time = 0.0

    with _audio_queue.mutex:
        _audio_queue.queue.clear()

    with sd.InputStream(
        samplerate=SAMPLERATE,
        channels=CHANNELS,
        dtype="float32",
        blocksize=BLOCKSIZE,
        callback=_audio_callback,
    ):
        for audio in _collector():
            energy = _rms(audio)
            seconds = len(audio) / SAMPLERATE

            if energy < SILENCE_THRESHOLD:
                silence_time += seconds
                if silence_time >= MAX_SILENCE_SECONDS:
                    break
                continue

            silence_time = 0.0
            audio = _normalize(audio)

            inputs = whisper_processor(
                audio,
                sampling_rate=SAMPLERATE,
                return_tensors="pt",
            ).input_features.to(device)

            with torch.no_grad():
                ids = whisper_model.generate(
                    inputs,
                    task="transcribe",
                    language="en",
                    do_sample=False,
                    temperature=0.0,
                )

            text = whisper_processor.batch_decode(
                ids, skip_special_tokens=True
            )[0].strip()

            if text:
                transcript.append(text)

    return " ".join(transcript).strip()
