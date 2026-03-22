import random
import mysql.connector
import os
from dotenv import load_dotenv


load_dotenv()

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("DB_PASSWORD"),
    database="triage_db"
)

cursor = conn.cursor()

symptoms = [
    "chest pain", "breathing issue", "dizziness",
    "fever", "fainting", "low oxygen", "sweating"
]

types = ["cardiac", "emergency", "irrelevant", "chronic"]

for i in range(1000):
    text = f"Patient has {random.choice(symptoms)} with {random.choice(['mild','severe','sudden'])} condition"
    year = random.randint(2010, 2025)
    t = random.choice(types)

    cursor.execute(
        "INSERT INTO patient_history (text, year, type) VALUES (%s, %s, %s)",
        (text, year, t)
    )

conn.commit()
conn.close()

print("✅ 1000 records inserted")