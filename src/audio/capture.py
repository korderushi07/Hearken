import pyaudiowpatch as pyaudio
import numpy as np
from scipy.signal import resample_poly
from fractions import Fraction

SAMPLE_RATE = 16000
CHUNK_SECONDS = 5


def capture_audio_chunk():
    audio = pyaudio.PyAudio()
    stream = None

    try:
        device = next(audio.get_loopback_device_info_generator())
        device_index = device["index"]
        original_rate = int(device["defaultSampleRate"])
        channels = 2

        print(f"Listening to: {device['name']}")
        print(f"Capturing {CHUNK_SECONDS} seconds of system audio...")

        stream = audio.open(
            format=pyaudio.paInt16,
            channels=channels,
            rate=original_rate,
            input=True,
            input_device_index=device_index,
            frames_per_buffer=1024,
        )

        frames = []

        for _ in range(int(original_rate * CHUNK_SECONDS / 1024) + 1):
            frames.append(
                stream.read(1024, exception_on_overflow=False)
            )

        samples = np.frombuffer(b"".join(frames), dtype=np.int16)
        samples = samples.reshape(-1, channels)

        # Convert stereo audio to mono.
        mono = samples.mean(axis=1).astype(np.float32) / 32768.0

        # Convert the sample rate to 16 kHz for Whisper.
        ratio = Fraction(SAMPLE_RATE, original_rate)
        converted = resample_poly(
            mono, ratio.numerator, ratio.denominator
        )

        print("Audio captured successfully!")
        return converted

    finally:
        if stream is not None:
            stream.stop_stream()
            stream.close()
        audio.terminate()


if __name__ == "__main__":
    capture_audio_chunk()