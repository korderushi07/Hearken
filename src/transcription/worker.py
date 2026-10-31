import threading
import numpy as np

from PySide6.QtCore import QThread, Signal
from faster_whisper import WhisperModel

from src.audio.capture import capture_audio_chunk
from src.detection.name_detector import detect_name
from src.detection.keyword_detector import detect_keywords
from src.notifications.notifier import send_notification
from src.notifications.cooldown import should_alert


class AudioWorker(QThread):

    status_changed = Signal(str)
    alert_detected = Signal(str, str)
    error_occurred = Signal(str)

    def __init__(self):
        super().__init__()
        self.stop_event = threading.Event()

    def stop(self):
        self.stop_event.set()

    def run(self):
        try:
            self.status_changed.emit("Loading Whisper model...")

            model = WhisperModel(
                "small",
                device="cpu",
                compute_type="int8"
            )

            self.status_changed.emit("Listening to system audio...")

            while not self.stop_event.is_set():

                audio = capture_audio_chunk()

                if self.stop_event.is_set():
                    break

                audio_level = np.sqrt(np.mean(audio ** 2))

                if audio_level < 0.005:
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

                last_name_end = -1

                for segment in segments:

                    if self.stop_event.is_set():
                        break

                    text = segment.text.strip()

                    if not text:
                        continue

                    # Name detection
                    if detect_name(text):

                        if segment.start >= last_name_end - 0.2:
                            last_name_end = segment.end

                            send_notification(
                                "PingMe - Name Mentioned",
                                "Someone mentioned Rushikesh!"
                            )

                            self.alert_detected.emit(
                                "Name Mentioned",
                                text
                            )

                    # Keyword detection
                    keywords = detect_keywords(text)

                    for keyword in keywords:

                        if should_alert(f"keyword:{keyword}"):

                            send_notification(
                                "PingMe - Keyword Alert",
                                f"Keyword detected: {keyword}"
                            )

                            self.alert_detected.emit(
                                "Keyword: " + keyword,
                                text
                            )

            self.status_changed.emit("Stopped")

        except Exception as error:
            self.error_occurred.emit(str(error))
            self.status_changed.emit("Error")
