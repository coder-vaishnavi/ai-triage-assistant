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

# 🔥 Create 50 patients
patient_names = [f"Patient_{i}" for i in range(1, 51)]

for i in range(1000):
    patient_id = random.randint(1, 50)
    patient_name = patient_names[patient_id - 1]

    text = f"{patient_name} has {random.choice(symptoms)} with {random.choice(['mild','severe','sudden'])} condition"
    year = random.randint(2010, 2025)
    t = random.choice(types)

    cursor.execute(
        "INSERT INTO patient_history (patient_id, patient_name, text, year, type) VALUES (%s, %s, %s, %s, %s)",
        (patient_id, patient_name, text, year, t)
    )

conn.commit()
conn.close()

print("✅ 1000 patient records inserted successfully")