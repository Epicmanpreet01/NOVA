import torch
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq
from kokoro import KPipeline


device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.float16 if device == "cuda" else torch.float32


AUDIO_MODEL_ID = "openai/whisper-small"

print("[AUDIO] Loading Whisper model...")

whisper_processor = AutoProcessor.from_pretrained(AUDIO_MODEL_ID)
whisper_model = AutoModelForSpeechSeq2Seq.from_pretrained(
    AUDIO_MODEL_ID,
    torch_dtype=dtype
).to(device)

whisper_model.eval()

print("[AUDIO] Whisper loaded")


print("[AUDIO] Loading Kokoro TTS...")

kokoro_pipeline = KPipeline(
    lang_code="a",
    repo_id="hexgrad/Kokoro-82M"
)

print("[AUDIO] Kokoro loaded")
