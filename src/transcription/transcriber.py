from faster_whisper import WhisperModel
from src.audio.capture import capture_audio_chunk


def main():
    print("Loading Whisper model...")
    model = WhisperModel("base", device="cpu", compute_type="int8")
    print("Model loaded!\n")

    while True:
        try:
            audio = capture_audio_chunk()

            segments, info = model.transcribe(
                audio,
                language=None,
                vad_filter=True
            )

            print(f"\nDetected language: {info.language}")

            for segment in segments:
                if segment.text.strip():
                    print("Transcript:", segment.text.strip())

        except KeyboardInterrupt:
            print("\nStopped listening.")
            break


if __name__ == "__main__":
    main()