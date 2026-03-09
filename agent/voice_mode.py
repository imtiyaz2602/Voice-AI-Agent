import speech_recognition as sr
import pyttsx3
import time

from agent.voice_agent import agent_response


recognizer = sr.Recognizer()


def speak(text):

    engine = pyttsx3.init()

    engine.setProperty("rate", 170)

    text = str(text)

    print("AI:", text)

    engine.say(text)

    engine.runAndWait()

    engine.stop()

    time.sleep(0.5)


def listen():

    with sr.Microphone() as source:

        print("🎤 Listening...")

        recognizer.adjust_for_ambient_noise(source, duration=1)

        audio = recognizer.listen(source, phrase_time_limit=6)

        try:

            text = recognizer.recognize_google(audio)

            print("You:", text)

            return text

        except sr.UnknownValueError:

            print("Sorry, I didn't understand.")

            return None


def run_voice_agent():

    speak("Hello. Welcome to the hospital appointment assistant. How can I help you today?")

    while True:

        user_input = listen()

        if not user_input:
            continue

        text = user_input.lower()

        # greeting detection
        if any(greet in text for greet in ["hi", "hello", "hey"]):

            speak("Hello. How can I help you today?")

            continue

        # exit command
        if text in ["exit", "quit", "stop", "bye"]:

            speak("Goodbye. Have a great day.")

            break

        # send to AI agent
        response = agent_response(user_input)

        speak(response)


if __name__ == "__main__":

    run_voice_agent()