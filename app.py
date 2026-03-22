from flask import Flask, render_template, request, jsonify, redirect, session
from model import process_query
from db import log_query, get_connection
from auth import register_doctor, login_doctor
import json
import re
import time

app = Flask(__name__)
app.secret_key = "secret123"  # change later for security

# ===================== HOME =====================
@app.route("/")
def home():
    return render_template("login.html")


# ===================== AUTH =====================

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form
        user = login_doctor(data["email"], data["password"])

        if user:
            session["user"] = user
            return redirect("/dashboard")
        else:
            return "Invalid credentials"

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        data = request.form

        register_doctor(
            data["name"],
            data["email"],
            data["password"],
            data["specialization"]
        )

        return redirect("/login")

    return render_template("signup.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ===================== DASHBOARD =====================

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    return render_template("dashboard.html", user=session["user"])



# ===================== JSON EXTRACT =====================

def extract_json(text):
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        return match.group()
    return None


# ===================== TRIAGE API =====================

@app.route("/triage", methods=["POST"])
def triage():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    query = request.json.get("query")

    start = time.time()

    llm_output, context = process_query(query)

    end = time.time()
    latency = round((end - start) * 1000, 2)

    print("RAW LLM:", llm_output)

    try:
        json_text = extract_json(llm_output)

        if json_text:
            parsed = json.loads(json_text)
        else:
            raise ValueError("No JSON")

    except:
        parsed = {
            "severity": "UNKNOWN",
            "action": llm_output,
            "reason": "Parsing error"
        }

    parsed["severity"] = parsed.get("severity", "UNKNOWN").upper()

    # 🔥 LOG QUERY
    log_query(query, str(parsed))

    # 🔥 SAVE TO PATIENT TABLE
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO patients (name, symptoms, diagnosis) VALUES (%s, %s, %s)",
        (session["user"]["name"], query, parsed["severity"])
    )

    conn.commit()
    conn.close()

    return jsonify({
        "severity": parsed.get("severity"),
        "action": parsed.get("action"),
        "reason": parsed.get("reason"),
        "context": context,
        "latency": latency,
        "original_records": 5,
        "pruned_records": len(context)
    })


# ===================== PATIENT HISTORY =====================

@app.route("/patients")
def patients():
    if "user" not in session:
        return redirect("/login")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM patients ORDER BY created_at DESC")
    data = cursor.fetchall()

    conn.close()

    return render_template("patients.html", patients=data)


# ===================== RUN =====================

if __name__ == "__main__":
    app.run(debug=True)