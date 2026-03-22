from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from db import fetch_data
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Load data
data = fetch_data()
texts = [item["text"] for item in data]
# 🔥 SAFE MODEL LOADING
def load_model():
    try:
        print("Loading model (online)...")
        return SentenceTransformer('all-MiniLM-L6-v2')
    except Exception as e:
        print("⚠️ Online failed, using offline cache...")
        return SentenceTransformer('all-MiniLM-L6-v2', local_files_only=True)
model = load_model()
embeddings = model.encode(texts)

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))


# 🔍 SEARCH
def search(query, k=5):
    query_embedding = model.encode([query])
    D, I = index.search(np.array(query_embedding), k)
    return [data[i] for i in I[0]]


# ✂️ CONTEXT PRUNING
def filter_time(docs):
    return [d for d in docs if d["year"] >= 2018]


def priority_score(text):
    text = text.lower()
    score = 0
    if "chest" in text: score += 4
    if "breath" in text: score += 4
    if "oxygen" in text: score += 4
    if "faint" in text: score += 4
    if "sweating" in text: score += 3
    if "dizziness" in text: score += 2
    return score


def prune_context(docs):
    docs = filter_time(docs)

    scored = [(doc, priority_score(doc["text"])) for doc in docs]
    scored.sort(key=lambda x: x[1], reverse=True)

    seen = set()
    unique_docs = []

    for doc, _ in scored:
        if doc["text"] not in seen:
            unique_docs.append(doc["text"])
            seen.add(doc["text"])
        if len(unique_docs) == 3:
            break

    return unique_docs


# 🤖 GROQ LLM (FREE 🔥)
def llm_decision(query, context):

    prompt = f"""
You are a medical triage assistant.

Patient symptoms: {query}
Relevant history: {context}

IMPORTANT:
- Respond ONLY with valid JSON
- Do NOT include explanation
- Do NOT use ```json

Format:
{{
    "severity": "HIGH or MEDIUM or LOW",
    "action": "short action",
    "reason": "short explanation"
}}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content


# 🚀 PIPELINE
def process_query(query):
    results = search(query)
    pruned = prune_context(results)

    context_text = " ".join(pruned)

    llm_output = llm_decision(query, context_text)

    return llm_output, pruned