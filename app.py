from __future__ import annotations
import json, re
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).parent
DATA = ROOT / "data" / "email_assistant_dataset.csv"
SAVED = ROOT / "outputs" / "generated_replies.jsonl"
OLLAMA_URL = "http://localhost:11434/api/generate"

st.set_page_config(page_title="Intelligent Email Assistant", page_icon="✉️", layout="wide")
st.title("✉️ Intelligent Email Assistant")
st.caption("Sahana · URK23CS1206 | Experiment 3 · Context-aware customer support")

@st.cache_data
def load_data():
    return pd.read_csv(DATA).fillna("")

def words(text):
    return set(re.findall(r"[a-z0-9]+", str(text).lower()))

def similar_records(query, df, n=3):
    q = words(query)
    scored = []
    for _, row in df.iterrows():
        d = words(f"{row['Subject']} {row['Customer_Email']} {row['Intent']}")
        score = len(q & d) / max(1, len(q | d))
        scored.append((score, row))
    return sorted(scored, key=lambda x: x[0], reverse=True)[:n]

def ollama(prompt, model):
    import urllib.request
    payload = json.dumps({"model": model, "prompt": prompt, "stream": False}).encode()
    req = urllib.request.Request(OLLAMA_URL, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=75) as response:
        return json.loads(response.read()).get("response", "").strip()

def save_reply(record):
    SAVED.parent.mkdir(parents=True, exist_ok=True)
    with SAVED.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

with st.sidebar:
    st.header("Assistant settings")
    model = st.text_input("Ollama model", "llama3.2")
    tone = st.selectbox("Reply tone", ["Friendly", "Formal", "Empathetic"])
    st.caption("Ollama is optional. If unavailable, the assistant uses a local fallback reply.")

left, right = st.columns([1, 1])
with left:
    st.subheader("Customer email")
    customer = st.text_input("Customer name", "Joh")
    subject = st.text_input("Subject", "Delivery Delay")
    email = st.text_area("Email message", "My package has not arrived yet.", height=150)
    generate = st.button("Generate assistant reply", type="primary", use_container_width=True)
with right:
    st.subheader("Conversation summary")
    st.caption("A concise summary is generated from the current email and suggested response.")

df = load_data()
if generate and email.strip():
    matches = similar_records(f"{subject} {email}", df)
    best = matches[0][1]
    prompt = (f"Write a concise {tone.lower()} customer support reply to {customer}. "
              f"Subject: {subject}. Customer message: {email}. Related past reply: {best['Previous_Reply']}. "
              "Do not invent order details or promise a specific outcome.")
    try:
        reply = ollama(prompt, model)
        source = f"Ollama ({model})"
    except Exception:
        reply = (f"Hi {customer},\n\nThank you for reaching out. I’m sorry your package has not arrived yet. "
                 "Our team will check the shipment status and share an update as soon as possible. "
                 "Please let us know if you have any other details that could help us investigate.\n\nBest,\nCustomer Support")
        source = "Local fallback"
    st.session_state["assistant_result"] = {
        "customer": customer, "subject": subject, "email": email, "tone": tone,
        "model": model, "reply": reply, "intent": best["Intent"],
        "matches": [{"score": float(score), "email": row["Customer_Email"], "intent": row["Intent"], "reply": row["Previous_Reply"]}
                    for score, row in matches], "source": source
    }

result = st.session_state.get("assistant_result")
if result:
    st.info(f"Reply generated with {result['source']}.")
    with st.expander("Relevant past conversations", expanded=True):
        for match in result["matches"]:
            st.markdown(f"**{match['intent']}** · similarity {match['score']:.2f}")
            st.write(f"Customer: {match['email']}")
            st.write(f"Previous reply: {match['reply']}")
    st.markdown("### Suggested reply")
    result["reply"] = st.text_area("Review or edit reply before saving", result["reply"], height=190, key="reply_editor")
    st.markdown("### Summary")
    summary = (f"{result['customer']} contacted support about {result['subject'].lower()}. "
               f"They said: {result['email'].strip()} The assistant acknowledged the concern and provided a response "
               "based on relevant historical customer support conversations.")
    st.write(summary)
    if st.button("Save generated reply"):
        save_reply({**result, "summary": summary, "timestamp": datetime.now().isoformat(timespec="seconds")})
        st.success("Reply saved to outputs/generated_replies.jsonl")

st.divider()
st.caption(f"Reference dataset: {len(df)} historical email interactions · Retrieval uses token overlap (Jaccard similarity).")
