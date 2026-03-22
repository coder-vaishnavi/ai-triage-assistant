# 🚑 AI Triage Assistant

A real-time AI-powered triage assistant that analyzes patient symptoms and large medical history data to recommend the next best action instantly.

---

## 🧠 Overview

This project solves the problem of slow and noisy medical data analysis in emergency situations using Intelligent Context Pruning to filter irrelevant data and provide fast, accurate decisions.

---

## 🚀 Features

* ⚡ Fast triage system (low latency)
* 🧠 Intelligent Context Pruning (core technique)
* 🔍 FAISS-based semantic search
* 🤖 LLM-based reasoning (Groq API)
* 🏥 Doctor dashboard (login/signup)
* 📋 Patient history tracking
* 📊 Explainable output (severity, action, reason)

---

## 🧩 How It Works

1. User enters symptoms
2. FAISS retrieves relevant records
3. Context pruning reduces noise (1000 → 2–3 records)
4. LLM generates severity, action, and reasoning

---

## 📊 Results

* 📉 Context reduced: 1000 → 2–3 records
* ⚡ Response time: ~300–400ms
* 🧠 Improved relevance and accuracy

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

Create `.env`:

```
GROQ_API_KEY=your_api_key
DB_PASSWORD=your_mysql_password
```

Run:

```bash
python data_loader.py
python app.py
```

Open:

[http://127.0.0.1:5000/login](http://127.0.0.1:5000/login)

---

## 💡 Key Highlight

Reduces large medical datasets to minimal relevant context using intelligent pruning for real-time decision-making.

---

