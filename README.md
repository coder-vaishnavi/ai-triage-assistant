# 🚑 AI Triage Assistant

A real-time AI-powered triage assistant that analyzes patient symptoms and medical history to recommend the next best action instantly.

---

## 🧠 Overview

This system solves slow and noisy medical data analysis in emergency scenarios using Intelligent Context Pruning. It reduces large datasets (1000+ records) to a few relevant ones for fast and accurate decision-making.

---

## 🚀 Features

* ⚡ Low-latency triage system
* 🧠 Intelligent Context Pruning
* 🔍 FAISS-based semantic search
* 🤖 LLM reasoning (Groq API)
* 🏥 Doctor login/signup dashboard
* 📋 Patient history tracking
* 👤 Patient-specific analysis

---

## 🧩 How It Works

1. Doctor logs into the system
2. Selects patient (via Patient ID)
3. Enters symptoms
4. FAISS retrieves relevant records
5. Context pruning reduces noise (1000 → 2–3 records)
6. LLM generates severity, action, and reasoning

---

## 📊 Results

* 📉 Context reduction: 1000 → 2–3 records
* ⚡ Latency: ~300–400ms
* 🧠 Improved relevance

---

## 🛠️ Tech Stack

Python, Flask, MySQL, FAISS, Sentence Transformers, Groq API, HTML, CSS, JavaScript

---

## ⚙️ Setup

```bash
git clone https://github.com/your-username/ai-triage-assistant.git
cd ai-triage-assistant
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

```

---

## 🔥 IMPORTANT (First Run)

```bash
python data_loader.py   # insert 1000 records
python model.py         # download & cache embedding model
```

---

## ▶️ Run App

```bash
python app.py
```

Open:
[http://127.0.0.1:5000/login](http://127.0.0.1:5000/login)

---

## 💡 Key Highlight

Uses Intelligent Context Pruning to reduce noise and enable real-time patient-specific triage decisions.

---
