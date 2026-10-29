# Intelligent Email Assistant — Experiment 3

**Student:** Sahana  
**Register number:** URK23CS1206

A local email assistant that finds similar past conversations in a 100-record dataset, proposes a professional response, supports three writing tones, summarizes the interaction, and saves reviewed replies locally. It can use a local Ollama model; a safe template reply is provided when Ollama is unavailable.

## Features

- Streamlit interface for customer name, subject, and message
- Similar conversation retrieval using Jaccard token similarity
- Optional Ollama generation (default model: `llama3.2`)
- Friendly, Formal, and Empathetic tones
- Editable assistant reply, summary, and JSONL persistence

## Requirements

- Python 3.10+
- Packages in `requirements.txt`
- Optional: Ollama running locally with a model such as `llama3.2`

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The app reads `data/email_assistant_dataset.csv`. The original workbook is included for reference. Generated replies are saved to `outputs/generated_replies.jsonl`.

## Project layout

```
app.py
requirements.txt
README.md
data/
screenshots/
outputs/
```

## Deployment

Deploy `app.py` from this repository on Streamlit Community Cloud. Cloud hosting cannot reach the Ollama service running on your computer, so the app falls back to its local reply template when no Ollama endpoint is available.
