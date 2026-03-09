from tools.appointment_tools import (
    book_appointment,
    cancel_appointment,
    reschedule_appointment,
    reset_appointments,
    show_appointments
)

DOCTOR_MAP = {
    "cardiologist": 1,
    "dermatologist": 2,
    "neurologist": 3,
    "orthopedic": 4,
    "general": 5
}


def agent_response(user_message):

    text = user_message.lower()

    if text == "reset":
        return reset_appointments()

    if "show appointments" in text:
        return show_appointments()

    if "cancel appointment for" in text:

        patient = text.replace("cancel appointment for", "").strip()

        return cancel_appointment(patient)

    if "reschedule" in text:

        parts = text.split()

        patient = parts[1]

        new_time = parts[-2] + " " + parts[-1]

        return reschedule_appointment(patient, new_time)

    if "book" in text:

        doctor = None

        for d in DOCTOR_MAP:

            if d in text:
                doctor = d
                break

        if not doctor:
            return "Which doctor would you like to book?"

        doctor_id = DOCTOR_MAP[doctor]

        time = "2026-03-10 10:00"

        if "for" in text:

            patient = text.split("for")[-1].strip()

        else:

            patient = "guest"

        return book_appointment(patient, doctor_id, time)

    return "I can help with booking, cancelling, rescheduling, or showing appointments."