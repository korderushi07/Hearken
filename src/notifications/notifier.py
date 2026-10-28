from winotify import Notification, audio


def send_notification(title: str, message: str):
    notification = Notification(
        app_id="PingMe - Meeting Alert",
        title=title,
        msg=message,
        duration="short",
    )

    notification.set_audio(audio.Default, loop=False)
    notification.show()