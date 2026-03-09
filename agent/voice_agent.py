appointments = []

state = {
    "intent": None,
    "doctor": None,
    "date": None,
    "time": None
}


def reset_state():
    state["intent"] = None
    state["doctor"] = None
    state["date"] = None
    state["time"] = None


def parse_doctor(text):
    if "cardio" in text:
        return "Cardiologist"
    if "derma" in text:
        return "Dermatologist"
    if "neuro" in text:
        return "Neurologist"
    return None


def parse_time(text):
    words = text.split()

    for w in words:
        if "am" in w or "pm" in w:
            return w
        if w.isdigit():
            return w

    return None


def parse_date(text):
    if "tomorrow" in text:
        return "tomorrow"
    if "today" in text:
        return "today"
    return None


def agent_response(user_input):

    text = user_input.lower()

    # -------- BOOK --------
    if "book" in text:
        reset_state()
        state["intent"] = "book"
        return "Which doctor would you like to book?"

    if state["intent"] == "book":

        doctor = parse_doctor(text)
        date = parse_date(text)
        time = parse_time(text)

        if doctor:
            state["doctor"] = doctor

        if date:
            state["date"] = date

        if time:
            state["time"] = time

        if not state["doctor"]:
            return "Please tell the doctor name (cardiologist, dermatologist, neurologist)."

        if not state["date"]:
            return "Please tell the date (today or tomorrow)."

        if not state["time"]:
            return "Please tell the appointment time."

        appointment = {
            "doctor": state["doctor"],
            "date": state["date"],
            "time": state["time"]
        }

        appointments.append(appointment)

        msg = f"Appointment booked with {state['doctor']} {state['date']} at {state['time']}"

        reset_state()

        return msg

    # -------- CANCEL --------
    if "cancel" in text:

        if not appointments:
            return "No appointments found."

        removed = appointments.pop()

        return f"Appointment with {removed['doctor']} cancelled."

    # -------- SHOW --------
    if "show" in text or "appointment" in text:

        if not appointments:
            return "No appointments booked."

        result = "Your appointments:\n"

        for a in appointments:
            result += f"{a['doctor']} {a['date']} at {a['time']}\n"

        return result

    # -------- RESCHEDULE --------
    if "reschedule" in text:

        if not appointments:
            return "No appointments to reschedule."

        state["intent"] = "reschedule"

        return "What new time would you like?"

    if state["intent"] == "reschedule":

        time = parse_time(text)

        if not time:
            return "Please provide a valid time."

        appointments[-1]["time"] = time

        reset_state()

        return f"Appointment rescheduled to {time}"

    # -------- DEFAULT --------
    return "I can help with booking, cancelling, rescheduling, or showing appointments."