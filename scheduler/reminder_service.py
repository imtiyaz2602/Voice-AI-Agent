import time
from datetime import datetime, timedelta

from database.db import get_connection
from voice.text_to_speech import speak


# keep track of reminders already sent
sent_reminders = set()


def check_reminders():

    try:

        conn = get_connection()
        cursor = conn.cursor()

        now = datetime.now()
        next_24_hours = now + timedelta(hours=24)

        # only fetch upcoming appointments
        cursor.execute(
            """
            SELECT patient_name, doctor_id, appointment_time
            FROM appointments
            WHERE appointment_time BETWEEN ? AND ?
            """,
            (now, next_24_hours)
        )

        appointments = cursor.fetchall()

        for patient_name, doctor_id, appointment_time in appointments:

            # convert string to datetime if needed
            if isinstance(appointment_time, str):
                appointment_time = datetime.fromisoformat(appointment_time)

            reminder_id = f"{patient_name}_{appointment_time}"

            if reminder_id in sent_reminders:
                continue

            message = (
                f"Hello {patient_name}. "
                f"This is a reminder for your appointment scheduled at "
                f"{appointment_time.strftime('%Y-%m-%d %H:%M')}."
            )

            print("REMINDER:", message)

            speak(message)

            # mark reminder as sent
            sent_reminders.add(reminder_id)

        conn.close()

    except Exception as e:

        print("Reminder error:", e)


def start_reminder_service():

    print("Reminder service started")

    while True:

        check_reminders()

        # check every 60 seconds
        time.sleep(60)