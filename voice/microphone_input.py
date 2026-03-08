import sounddevice as sd
import soundfile as sf


def record_audio(filename="input.wav", duration=4, samplerate=16000):

    print("🎤 Speak now...")

    try:
        # reset device (prevents freeze after TTS)
        sd.stop()

        recording = sd.rec(
            int(duration * samplerate),
            samplerate=samplerate,
            channels=1,
            dtype="float32"
        )

        sd.wait()

        sf.write(filename, recording, samplerate)

        print("Recording finished")

        return filename

    except Exception as e:
        print("Microphone error:", e)
        return None