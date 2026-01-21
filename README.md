# NOVA – Desktop AI Assistant

NOVA is a **desktop AI assistant and companion** designed to operate continuously in the background, respond to wake words, process voice commands, and interact through a rich animated UI.

The project has evolved over time and recently received a **major audio system upgrade**, replacing legacy speech recognition and text-to-speech components with a modern neural pipeline.

---

## Project Overview

NOVA combines:

- Wake word detection
- Voice command processing
- Conversational AI
- Desktop automation
- Animated UI (Eel + Web frontend)
- Modular, replaceable subsystems

The assistant is designed to work **even when the UI is not in focus** and to remain responsive with minimal latency.

---

## Core Features

- Always-listening wake word support
- Voice and text input
- Neural speech-to-text
- Neural text-to-speech
- Desktop automation (apps, media, system controls)
- Spotify, YouTube, WhatsApp integrations
- Conversational LLM backend
- Animated assistant UI
- Modular architecture for future expansion

---

## Recent Major Update: Audio Engine Upgrade

### What Changed

The original NOVA project used:

- `speech_recognition` (Google STT)
- `pyttsx3` (system TTS)

These components were **replaced** with a modern audio engine based on:

- **Whisper** for speech-to-text
- **Kokoro** for text-to-speech

This upgrade was done **without rewriting the command pipeline**, keeping backward compatibility while dramatically improving quality and reliability.

---

## New Audio Pipeline (Current)

### Speech-to-Text (ASR)

- Model: `openai/whisper-small`
- Offline inference
- Silence-based end-of-speech detection
- GPU acceleration when available
- No external API dependency

### Text-to-Speech (TTS)

- Engine: Kokoro
- Neural voice synthesis
- Stable, natural speech
- Blocking playback (prevents UI desync)

### Model Lifecycle

- Models are loaded **once at application startup**
- No lazy loading during interaction
- Predictable memory and latency behavior

---

## Backward Compatibility

The update preserves the original function signatures used across the project:

### Replaced Internally (No Call-Site Changes)

- `Speech(text)`
- `takeCommand()`

Existing command logic, UI hooks, and wake-word handling remain unchanged.

---

## High-Level Architecture

```
NOVA
├── Wake Word Engine (Porcupine)
├── Audio Engine
│   ├── Whisper (ASR)
│   └── Kokoro (TTS)
├── Command Router
├── Action Handlers
│   ├── Apps / Websites
│   ├── Media Control
│   ├── Spotify / YouTube
│   └── System Automation
├── Conversational LLM
├── UI Layer (Eel + Web)
└── Background Services
```

---

## Wake Word Behavior

- Runs independently of the UI
- Triggers the assistant even when the window is not focused
- Cooldown prevents accidental re-triggering
- Audio streams are cleanly separated from ASR capture

---

## UI Layer

- Built using Eel + HTML/CSS/JS
- Animated idle state
- Siri-style wave during listening
- Chat canvas for conversation history
- Keyboard and mouse shortcuts supported

---

## Requirements

### Python

- Python 3.9 – 3.11 recommended

### System

- Windows (primary target)
- Microphone input
- Audio output device
- Optional NVIDIA GPU

### Core Dependencies

```
torch
transformers
sounddevice
numpy
kokoro
pvporcupine
pyaudio
eel
```

---

## Running the Project

1. Set environment variables:
   - `GROQ_API_KEY`
   - `PICOVOICE_API_KEY`

2. Ensure models are downloaded on first run.

3. Launch NOVA:

   ```
   python run.py
   ```

4. Say the wake word to activate.

---

## Development Notes

- This project originated over two years ago and has been incrementally modernized.
- Some legacy code paths remain by design to preserve behavior.
- The recent audio refactor focused on **minimal disruption with maximum improvement**.
- Readability has been improved where possible without a full rewrite.

---

## Future Plans

- Streaming ASR
- Emotion-aware voice synthesis

---

## Disclaimer

This project is for personal and experimental use.
Ensure compliance with all third-party model licenses before redistribution.
