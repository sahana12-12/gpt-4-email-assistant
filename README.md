# Intelligent Email Assistant — Experiment 3

**Student:** Sahana  
**Register number:** URK23CS1206

A local email assistant that finds similar past conversations in a 100-record dataset, proposes a professional response, supports three writing tones, summarizes the interaction, and saves reviewed replies locally. It can use a local Ollama model; a safe template reply is provided when Ollama is unavailable.

## Features

- Streamlit interface for customer name, subject, and message
- Retrieval of related historical emails using Jaccard token similarity
- Optional Ollama generation (default model: `llama3.2`)
- Friendly, Formal, and Empathetic tone choices
- Editable assistant reply and concise conversation summary
- Save output to `outputs/generated_replies.jsonl`

## Requirements

- Python 3.10+
- Packages in `requirements.txt`
- Optional: Ollama installed and running locally, with a model pulled (for example `ollama pull llama3.2`)

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit. Enter a sample email and choose **Generate assistant reply**. You can edit the response and save it.

## Dataset

`data/email_assistant_dataset.xlsx` is the supplied experiment dataset. The app reads its CSV counterpart at `data/email_assistant_dataset.csv`, committed alongside it for straightforward execution. It contains 100 historical email records and their prior replies.

## Project layout

```
app.py
requirements.txt
README.md
data/
  email_assistant_dataset.csv
  email_assistant_dataset.xlsx
screenshots/
outputs/
```

## Deployment

This app is ready for Streamlit Community Cloud: push the repository, create a new app from the repository, choose `app.py`, and deploy. Community Cloud does not have access to a user's local Ollama service by default, so the app automatically uses its local template reply there. To use a model in a hosted deployment, configure a reachable inference endpoint and credentials, then update the generation client.

## Result

The email assistant was implemented with retrieval, response drafting, tone selection, summary, and local persistence. Ollama-backed generation is optional so the core program remains usable without cloud APIs.
