
import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
)
from PySide6.QtCore import Qt

from src.transcription.worker import AudioWorker


class PingMeWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("PingMe")
        self.setMinimumSize(800, 550)

        self.worker = None

        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 25, 30, 25)
        main_layout.setSpacing(20)

        # Header
        header = QHBoxLayout()

        title = QLabel("PingMe")
        title.setStyleSheet(
            "font-size: 30px; font-weight: bold;"
        )

        subtitle = QLabel("Meeting Mention Alert")
        subtitle.setStyleSheet(
            "color: gray; font-size: 13px;"
        )

        header.addWidget(title)
        header.addWidget(subtitle)
        header.addStretch()

        main_layout.addLayout(header)

        # Status card
        status_card = QFrame()
        status_card.setFrameShape(QFrame.Shape.StyledPanel)

        status_layout = QVBoxLayout(status_card)

        self.status_label = QLabel("● Not Listening")
        self.status_label.setStyleSheet(
            "font-size: 20px; font-weight: bold; color: gray;"
        )

        self.description_label = QLabel(
            "PingMe is currently inactive."
        )

        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.description_label)

        main_layout.addWidget(status_card)

        # Start / Stop button
        self.toggle_button = QPushButton("Start Listening")
        self.toggle_button.setMinimumHeight(45)
        self.toggle_button.clicked.connect(
            self.toggle_listening
        )

        main_layout.addWidget(self.toggle_button)

        # Recent alerts
        alerts_title = QLabel("Recent Alerts")
        alerts_title.setStyleSheet(
            "font-size: 20px; font-weight: bold;"
        )

        main_layout.addWidget(alerts_title)

        self.alerts_label = QLabel(
            "No alerts yet.\n"
            "Detected name and keyword mentions will appear here."
        )

        self.alerts_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.alerts_label.setStyleSheet(
            "color: gray; padding: 40px;"
        )

        main_layout.addWidget(self.alerts_label)

    # Start / Stop listening
    def toggle_listening(self):

        if self.worker is not None and self.worker.isRunning():
            self.stop_listening()
        else:
            self.start_listening()

    def start_listening(self):

        self.toggle_button.setEnabled(False)

        self.status_label.setText("● Starting...")
        self.status_label.setStyleSheet(
            "font-size: 20px; font-weight: bold; color: orange;"
        )

        self.description_label.setText(
            "Starting audio monitoring and loading Whisper..."
        )

        self.worker = AudioWorker()

        self.worker.status_changed.connect(
            self.update_status
        )

        self.worker.alert_detected.connect(
            self.add_alert
        )

        self.worker.error_occurred.connect(
            self.show_error
        )

        self.worker.finished.connect(
            self.on_worker_finished
        )

        self.worker.start()

    def stop_listening(self):

        self.status_label.setText("● Stopping...")
        self.status_label.setStyleSheet(
            "font-size: 20px; font-weight: bold; color: orange;"
        )

        self.description_label.setText(
            "Stopping audio monitoring..."
        )

        self.toggle_button.setEnabled(False)

        self.worker.stop()

    # Update status from worker
    def update_status(self, status):

        if status == "Loading Whisper model...":
            self.status_label.setText("● Loading Model")
            self.description_label.setText(status)

        elif status == "Listening to system audio...":
            self.status_label.setText("● Listening")
            self.status_label.setStyleSheet(
                "font-size: 20px; font-weight: bold; color: green;"
            )

            self.description_label.setText(
                "PingMe is monitoring your meeting audio."
            )

            self.toggle_button.setText("Stop Listening")
            self.toggle_button.setEnabled(True)

        elif status == "Stopped":
            self.status_label.setText("● Not Listening")
            self.status_label.setStyleSheet(
                "font-size: 20px; font-weight: bold; color: gray;"
            )

            self.description_label.setText(
                "PingMe is currently inactive."
            )

    # Display detected alerts
    def add_alert(self, alert_type, transcript):

        current_text = self.alerts_label.text()

        if current_text.startswith("No alerts yet."):
            current_text = ""

        new_alert = f"🔔 {alert_type}\n{transcript}\n\n"

        self.alerts_label.setText(
            new_alert + current_text
        )

        self.alerts_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft
        )

    # Display errors
    def show_error(self, error):

        self.status_label.setText("● Error")
        self.status_label.setStyleSheet(
            "font-size: 20px; font-weight: bold; color: red;"
        )

        self.description_label.setText(error)

    # Reset after worker exits
    def on_worker_finished(self):

        self.toggle_button.setText("Start Listening")
        self.toggle_button.setEnabled(True)

        if self.status_label.text() != "● Error":
            self.status_label.setText("● Not Listening")
            self.status_label.setStyleSheet(
                "font-size: 20px; font-weight: bold; color: gray;"
            )

            self.description_label.setText(
                "PingMe is currently inactive."
            )


def run_app():

    app = QApplication(sys.argv)

    window = PingMeWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    run_app()
