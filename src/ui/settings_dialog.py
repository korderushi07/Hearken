from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QTextEdit,
    QCheckBox,
    QPushButton,
    QMessageBox,
)

from src.settings_manager import load_settings, save_settings


class SettingsDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("PingMe Settings")
        self.setMinimumWidth(450)

        self.settings = load_settings()

        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout(self)
        form = QFormLayout()

        # User name
        self.name_input = QLineEdit(
            self.settings["user_name"]
        )

        form.addRow("Your Name:", self.name_input)

        # Name variations
        self.variations_input = QTextEdit()
        self.variations_input.setPlainText(
            ", ".join(self.settings["name_variations"])
        )
        self.variations_input.setMaximumHeight(80)

        form.addRow("Name Variations:", self.variations_input)

        # Watched keywords
        self.keywords_input = QTextEdit()
        self.keywords_input.setPlainText(
            ", ".join(self.settings["watched_keywords"])
        )
        self.keywords_input.setMaximumHeight(100)

        form.addRow("Watched Keywords:", self.keywords_input)

        layout.addLayout(form)

        # Alert preferences
        self.name_alerts = QCheckBox("Enable name alerts")
        self.name_alerts.setChecked(
            self.settings["name_alerts_enabled"]
        )

        self.keyword_alerts = QCheckBox("Enable keyword alerts")
        self.keyword_alerts.setChecked(
            self.settings["keyword_alerts_enabled"]
        )

        layout.addWidget(self.name_alerts)
        layout.addWidget(self.keyword_alerts)

        # Save button
        self.save_button = QPushButton("Save Settings")
        self.save_button.clicked.connect(self.save)

        layout.addWidget(self.save_button)

    def save(self):

        user_name = self.name_input.text().strip()

        if not user_name:
            QMessageBox.warning(
                self,
                "Invalid Name",
                "Please enter your name."
            )
            return

        variations = [
            item.strip()
            for item in self.variations_input.toPlainText().split(",")
            if item.strip()
        ]

        keywords = [
            item.strip().lower()
            for item in self.keywords_input.toPlainText().split(",")
            if item.strip()
        ]

        updated_settings = {
            "user_name": user_name,
            "name_variations": variations,
            "watched_keywords": list(dict.fromkeys(keywords)),
            "name_alerts_enabled": self.name_alerts.isChecked(),
            "keyword_alerts_enabled": self.keyword_alerts.isChecked()
        }

        save_settings(updated_settings)

        QMessageBox.information(
            self,
            "Settings Saved",
            "Your settings have been saved successfully."
        )

        self.accept()
