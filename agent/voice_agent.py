import json
import re
from datetime import datetime
from langdetect import detect

from agent.groq_llm import ask_ai

from tools.appointment_tools import (
    book_appointment,
    cancel_appointment,
    reschedule_appointment
)

from memory.conversation_memory import (
    add_message,
    get_recent_memory
)


DOCTOR_MAP = {
    "cardiologist": 1,
    "dermatologist": 2,
    "neurologist": 3,
    "orthopedic": 4,
    "general": 5
}

pending_booking = None


def detect_language(text):

    try:
        if len(text.split()) <= 2:
            return "en"
        return detect(text)

    except:
        return "en"


def extract_json(text):

    match = re.search(r"\{.*?\}", text, re.DOTALL)

    if not match:
        return None

    try:
        return json.loads(match.group())

    except:
        return None


def agent_response(user_message):

    global pending_booking   # ✅ declare once at top

    add_message("user", user_message)

    text = user_message.lower().strip()

    greetings = ["hello", "hi", "hey"]

    if any(word in text for word in greetings):

        response = "Hello! How can I help you today with your appointment?"

        add_message("assistant", response)

        return response

    if text in ["bye", "goodbye"]:

        response = "Goodbye! Have a great day."

        add_message("assistant", response)

        return response

    # waiting for patient name
    if pending_booking is not None:

        patient_name = user_message.strip()

        doctor_type = pending_booking["doctor_type"]
        time = pending_booking["time"]

        doctor_id = DOCTOR_MAP.get(doctor_type)

        result = book_appointment(
            patient_name,
            doctor_id,
            time
        )

        pending_booking = None

        add_message("assistant", result)

        return result

    language = detect_language(user_message)

    print("Detected language:", language)

    history = get_recent_memory()

    history_text = ""

    for msg in history:
        history_text += f"{msg['role']}: {msg['content']}\n"

    today = datetime.now().strftime("%Y-%m-%d")

    prompt = f"""
You are a hospital appointment assistant.

Today's date: {today}

Conversation history:
{history_text}

User request:
{user_message}

Decide the action.

Actions:
book
cancel
reschedule
general

If booking and patient name missing return patient_name null.

Return JSON like this:

{{
"action":"book",
"patient_name":null,
"doctor_type":"cardiologist",
"time":"2026-03-10 10:00"
}}

Return ONLY JSON.
"""

    ai_text = ask_ai([
        {"role": "system", "content": "Return only JSON."},
        {"role": "user", "content": prompt}
    ])

    print("AI RAW RESPONSE:", ai_text)

    data = extract_json(ai_text)

    if not data:
        return "AI response parsing failed"

    action = data.get("action")

    if action == "book":

        patient = data.get("patient_name")
        doctor_type = data.get("doctor_type", "").lower()
        time = data.get("time")

        if patient is None:

            pending_booking = {
                "doctor_type": doctor_type,
                "time": time
            }

            return "What is the patient name?"

        doctor_id = DOCTOR_MAP.get(doctor_type)

        if doctor_id is None:
            return "Unknown doctor type"

        result = book_appointment(
            patient,
            doctor_id,
            time
        )

    elif action == "cancel":

        patient = data.get("patient_name")

        result = cancel_appointment(patient)

    elif action == "reschedule":

        patient = data.get("patient_name")
        time = data.get("time")

        result = reschedule_appointment(
            patient,
            time
        )

    else:

        result = data.get(
            "message",
            "I can help with booking, cancelling, or rescheduling appointments."
        )

    add_message("assistant", result)

    return result