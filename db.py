import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("DB_PASSWORD"),
        database="triage_db"
    )

def fetch_data():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM patient_history")
    data = cursor.fetchall()
    conn.close()
    return data

def log_query(query, response):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO logs (query, response) VALUES (%s, %s)",
        (query, response)
    )
    conn.commit()
    conn.close()