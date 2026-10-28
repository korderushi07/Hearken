from faster_whisper import WhisperModel
from src.audio.capture import capture_audio_chunk
from src.detection.name_detector import detect_name


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

            # Process transcription results
            for segment in segments:
                text = segment.text.strip()

                if not text:
                    continue

                print("Transcript:", text)

                if detect_name(text):
                    print("\n🔔 ALERT: Someone mentioned Rushikesh!\n")

        except KeyboardInterrupt:
            print("\nStopped listening.")
            break


if __name__ == "__main__":
    main()