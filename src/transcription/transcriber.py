from faster_whisper import WhisperModel
from src.audio.capture import capture_audio_chunk
from src.detection.name_detector import detect_name
from src.detection.keyword_detector import detect_keywords
from src.notifications.notifier import send_notification
from src.notifications.cooldown import should_alert


def main():
    print("Loading Whisper model...")
    model = WhisperModel("small", device="cpu", compute_type="int8")
    print("Model loaded!\n")

    while True:
        try:
            audio = capture_audio_chunk()

            segments, info = model.transcribe(
                audio,
                language=None,
                task="transcribe",
                vad_filter=True,
                beam_size=5,
                best_of=5,
                condition_on_previous_text=False,
                temperature=0.0
            )

            print(
                f"Detected language: {info.language} "
                f"(confidence: {info.language_probability:.2f})"
)

            # Process transcription results
            for segment in segments:
                text = segment.text.strip()

                if not text:
                    continue

                print("Transcript:", text)

                if detect_name(text) and should_alert("name"):
                    print("\n🔔 ALERT: Someone mentioned Rushikesh!\n")
                    send_notification(
                        "PingMe - Name Mentioned",
                        "Someone mentioned Rushikesh in the meeting!"
                )

                keywords = detect_keywords(text)

                for keyword in keywords:
                    if should_alert(f"keyword:{keyword}"):
                        send_notification(
                            "PingMe - Keyword Alert",
                            f"Keyword detected: {keyword}"
                        )
                        print(f"\n🔔 KEYWORD ALERT: {keyword}\n")

        except KeyboardInterrupt:
            print("\nStopped listening.")
            break


if __name__ == "__main__":
    main()