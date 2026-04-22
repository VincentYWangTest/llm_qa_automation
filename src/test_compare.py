import pandas as pd
import os
from config import get_client
from utils import log, Timer

os.makedirs("../reports", exist_ok=True)

def get_answer(client, model, q):
    try:
        resp = client.chat.completions.create(model=model, messages=[{"role":"user","content":q}])
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

def run_compare():
    questions = [
        "What is RAG?",
        "What is LLM hallucination?",
        "What is prompt injection?"
    ]
    results = []
    with Timer("Model Comparison"):
        for q in questions:
            row = {"question": q}
            client, model = get_client("deepseek")
            row["deepseek_answer"] = get_answer(client, model, q)
            log(f"Answered: {q[:30]}...")
            results.append(row)
    pd.DataFrame(results).to_csv("../reports/model_comparison.csv", index=False)
    log("✅ Comparison report saved")

if __name__ == "__main__":
    run_compare()