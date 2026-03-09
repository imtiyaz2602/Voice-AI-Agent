from database.db import get_connection
from datetime import datetime, timedelta


def book_appointment(patient_name, doctor_id, appointment_time):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        appointment_time = datetime.fromisoformat(appointment_time)

        cursor.execute(
            """
            SELECT * FROM appointments
            WHERE doctor_id = ? AND appointment_time = ?
            """,
            (doctor_id, appointment_time)
        )

        existing = cursor.fetchone()

        if existing:

            next_slot = appointment_time + timedelta(hours=1)

            return (
                f"That slot is already booked. "
                f"The next available slot is "
                f"{next_slot.strftime('%Y-%m-%d %H:%M')}."
            )

        cursor.execute(
            """
            INSERT INTO appointments (patient_name, doctor_id, appointment_time)
            VALUES (?, ?, ?)
            """,
            (patient_name, doctor_id, appointment_time)
        )

        conn.commit()

        return (
            f"Appointment booked successfully for {patient_name} "
            f"on {appointment_time.strftime('%Y-%m-%d')} "
            f"at {appointment_time.strftime('%H:%M')}."
        )

    except Exception as e:

        return f"Booking error: {e}"

    finally:

        conn.close()


def cancel_appointment(patient_name):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            "SELECT * FROM appointments WHERE patient_name = ?",
            (patient_name,)
        )

        appt = cursor.fetchone()

        if not appt:
            return f"No appointment found for {patient_name}."

        cursor.execute(
            "DELETE FROM appointments WHERE patient_name = ?",
            (patient_name,)
        )

        conn.commit()

        return f"Appointment cancelled successfully for {patient_name}."

    finally:

        conn.close()


def reschedule_appointment(patient_name, new_time):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            "SELECT * FROM appointments WHERE patient_name = ?",
            (patient_name,)
        )

        appt = cursor.fetchone()

        if not appt:
            return "No appointment found."

        cursor.execute(
            """
            UPDATE appointments
            SET appointment_time = ?
            WHERE patient_name = ?
            """,
            (new_time, patient_name)
        )

        conn.commit()

        return f"Appointment rescheduled to {new_time}."

    finally:

        conn.close()


def reset_appointments():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM appointments")

    conn.commit()

    conn.close()

    return "All appointments cleared."


def show_appointments():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT patient_name, doctor_id, appointment_time FROM appointments"
    )

    rows = cursor.fetchall()

    conn.close()

    if not rows:
        return "No appointments found."

    result = "Appointments:\n"

    for r in rows:
        result += f"{r[0]} | Doctor {r[1]} | {r[2]}\n"

    return result