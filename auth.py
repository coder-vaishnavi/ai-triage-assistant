from db import get_connection

def register_doctor(name, email, password, specialization):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO doctors (name, email, password, specialization) VALUES (%s,%s,%s,%s)",
        (name, email, password, specialization)
    )

    conn.commit()
    conn.close()


def login_doctor(email, password):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM doctors WHERE email=%s AND password=%s",
        (email, password)
    )

    user = cursor.fetchone()
    conn.close()
    return user