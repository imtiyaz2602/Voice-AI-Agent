import speech_recognition as sr
import pyttsx3
from voice_agent import agent_response
import time

recognizer = sr.Recognizer()
engine = pyttsx3.init()

engine.setProperty("rate", 170)


def speak(text):
    text = str(text)

    print("AI:", text)

    engine.say(text)
    engine.runAndWait()

    # small pause so microphone doesn't capture AI voice
    time.sleep(0.5)


def listen():

    with sr.Microphone() as source:

        print("🎤 Listening...")

        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)

            print("You:", text)

            return text

        except sr.UnknownValueError:
            return None


def run_voice_agent():

    speak("Hello. How can I help you?")

    while True:

        user_input = listen()

        if not user_input:
            continue

        if user_input.lower() in ["exit", "quit", "stop"]:
            speak("Goodbye")
            break

        response = agent_response(user_input)

        # ensure response is string
        response = str(response)

        speak(response)


if __name__ == "__main__":
    run_voice_agent()