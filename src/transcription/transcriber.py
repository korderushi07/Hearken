from faster_whisper import WhisperModel
from src.audio.capture import capture_audio_chunk
from src.detection.name_detector import detect_name
from src.detection.keyword_detector import detect_keywords
from src.notifications.notifier import send_notification
from src.notifications.cooldown import should_alert
import numpy as np


def main():
    print("Loading Whisper model...")
    model = WhisperModel("small", device="cpu", compute_type="int8")
    print("Model loaded!\n")

    while True:
        try:
            audio = capture_audio_chunk()
            audio_level = np.sqrt(np.mean(audio ** 2))

            SILENCE_THRESHOLD = 0.005

            if audio_level < SILENCE_THRESHOLD:
                print("Silence detected. Skipping transcription.\n")
                continue
            

            segments, info = model.transcribe(
                audio,
                language="en",
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
            last_name_end = -1
            for segment in segments:
                text = segment.text.strip()

                print(
                f"Segment: {segment.start:.2f}s - {segment.end:.2f}s | {text}"
            )

                if not text:
                    continue

                print("Transcript:", text)

                name_detected = detect_name(text)
                print(f"Name detected: {name_detected}")

                if name_detected:
                    # Skip duplicate detections from overlapping segments.
                    if segment.start < last_name_end - 0.2:
                        print("Duplicate name detection skipped.")
                    else:
                        last_name_end = segment.end

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