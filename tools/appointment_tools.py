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
            """
            SELECT * FROM appointments
            WHERE patient_name = ?
            """,
            (patient_name,)
        )

        appointment = cursor.fetchone()

        if not appointment:
            return f"No appointment found for {patient_name}."

        cursor.execute(
            """
            DELETE FROM appointments
            WHERE patient_name = ?
            """,
            (patient_name,)
        )

        conn.commit()

        return f"Appointment cancelled successfully for {patient_name}."

    except Exception as e:

        return f"Cancel error: {e}"

    finally:

        conn.close()


def reschedule_appointment(patient_name, new_time):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        new_time = datetime.fromisoformat(new_time)

        cursor.execute(
            """
            SELECT * FROM appointments
            WHERE patient_name = ?
            """,
            (patient_name,)
        )

        appointment = cursor.fetchone()

        if not appointment:
            return "No appointment found to reschedule."

        cursor.execute(
            """
            UPDATE appointments
            SET appointment_time = ?
            WHERE patient_name = ?
            """,
            (new_time, patient_name)
        )

        conn.commit()

        return (
            f"Appointment rescheduled successfully for {patient_name} "
            f"to {new_time.strftime('%Y-%m-%d %H:%M')}."
        )

    except Exception as e:

        return f"Reschedule error: {e}"

    finally:

        conn.close()