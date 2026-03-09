import sqlite3


def get_connection():

    conn = sqlite3.connect("hospital.db")

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT,
            doctor_id INTEGER,
            appointment_time TEXT
        )
        """
    )

    return conn