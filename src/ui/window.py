import sys
from datetime import datetime

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QListWidget,
    QListWidgetItem,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from src.transcription.worker import AudioWorker
from src.ui.settings_dialog import SettingsDialog


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

        self.settings_button = QPushButton("⚙ Settings")
        self.settings_button.clicked.connect(
            self.open_settings
        )

        header.addWidget(title)
        header.addWidget(subtitle)
        header.addStretch()
        header.addWidget(self.settings_button)

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

        self.empty_label = QLabel(
            "No alerts yet.\n"
            "Detected name and keyword mentions will appear here."
        )

        self.empty_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.empty_label.setStyleSheet(
            "color: gray; padding: 40px;"
        )

        main_layout.addWidget(self.empty_label)

        self.alert_list = QListWidget()
        self.alert_list.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                border: none;
                outline: none;
            }

            QListWidget::item {
                background-color: #2b2b2b;
                border-radius: 8px;
                padding: 14px;
                margin-bottom: 8px;
            }
        """)

        self.alert_list.hide()
        main_layout.addWidget(self.alert_list)

    # Open settings dialog
    def open_settings(self):
        dialog = SettingsDialog(self)
        dialog.exec()

    # Start / Stop
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
            "Loading Whisper and starting audio monitoring..."
        )

        self.worker = AudioWorker()

        self.worker.status_changed.connect(self.update_status)
        self.worker.alert_detected.connect(self.add_alert)
        self.worker.error_occurred.connect(self.show_error)
        self.worker.finished.connect(self.on_worker_finished)

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

    # Update status
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

    # Add alert to history
    def add_alert(self, alert_type, transcript):

        timestamp = datetime.now().strftime("%I:%M:%S %p")

        item = QListWidgetItem(
            f"🔔  {alert_type}                         {timestamp}\n"
            f"      {transcript}"
        )

        if alert_type == "Name Mentioned":
            item.setForeground(QColor("#4CAF50"))
        else:
            item.setForeground(QColor("#64B5F6"))

        self.alert_list.insertItem(0, item)

        while self.alert_list.count() > 50:
            self.alert_list.takeItem(self.alert_list.count() - 1)

        self.empty_label.hide()
        self.alert_list.show()

    # Show errors
    def show_error(self, error):

        self.status_label.setText("● Error")
        self.status_label.setStyleSheet(
            "font-size: 20px; font-weight: bold; color: red;"
        )

        self.description_label.setText(error)

    # Worker finished
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
