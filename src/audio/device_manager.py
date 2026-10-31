from pycaw.pycaw import AudioUtilities
import pyaudiowpatch as pyaudio


def get_default_loopback_device():
    """Find the loopback device matching Windows' default output."""

    default_device = AudioUtilities.GetSpeakers()
    default_name = default_device.FriendlyName

    audio = pyaudio.PyAudio()

    try:
        devices = list(audio.get_loopback_device_info_generator())

        # Match the Windows output name with its loopback device.
        for device in devices:
            loopback_name = device["name"].replace(" [Loopback]", "")

            if loopback_name.lower() == default_name.lower():
                print(f"Selected audio device: {device['name']}")
                return device

        raise RuntimeError(
            f"No loopback device found for: {default_name}"
        )

    finally:
        audio.terminate()


if __name__ == "__main__":
    device = get_default_loopback_device()
    print("Device index:", device["index"])
