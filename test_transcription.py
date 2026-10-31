from faster_whisper import WhisperModel

AUDIO_FILE = r"C:\Users\LOQ\Desktop\WhatsApp Ptt 2026-10-28 at 10.07.42 PM.ogg"

print("Loading Whisper model...")
model = WhisperModel("small", device="cpu", compute_type="int8")

print("Transcribing original audio...\n")

segments, info = model.transcribe(
    AUDIO_FILE,
    language="en",
    task="transcribe",
    vad_filter=True,
    beam_size=5,
    best_of=5,
    condition_on_previous_text=False,
    temperature=0.0
)

for segment in segments:
    print(segment.text.strip())