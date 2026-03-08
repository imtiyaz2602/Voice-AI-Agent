import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from voice.microphone_input import record_audio
from voice.speech_to_text import transcribe_audio
from agent.voice_agent import agent_response
from voice.text_to_speech import speak


print("Voice AI Agent started. Speak now...")


while True:

    try:

        # Record user speech
        record_audio("input.wav")

        # Start latency measurement
        stt_start = time.time()

        # Convert speech to text
        text = transcribe_audio("input.wav")

        stt_time = time.time() - stt_start

        if not text.strip():
            print("No speech detected")
            continue

        print("User:", text)

        # Exit commands
        exit_words = ["exit", "quit", "bye", "goodbye", "stop", "thank you"]

        if any(word in text.lower() for word in exit_words):
            speak("Goodbye. Ending session.")
            print("Session ended.")
            break

        # AI reasoning
        agent_start = time.time()

        response = agent_response(text)

        agent_time = time.time() - agent_start

        print("AI:", response)

        # Text to speech
        tts_start = time.time()

        speak(response)

        tts_time = time.time() - tts_start

        # Latency calculation
        total_latency = stt_time + agent_time + tts_time

        print("\nLatency Breakdown")
        print("STT:", round(stt_time, 3))
        print("Agent:", round(agent_time, 3))
        print("TTS:", round(tts_time, 3))
        print("Total:", round(total_latency, 3), "seconds\n")

    except KeyboardInterrupt:
        print("\nSession interrupted by user.")
        break

    except Exception as e:
        print("Error:", e)