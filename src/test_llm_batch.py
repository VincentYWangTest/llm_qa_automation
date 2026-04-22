import pandas as pd
import os
import re
import sys
from config import get_client
from report_generator import generate_batch_pdf
from visualizer import plot_hallucination_pie
from utils import log, Timer

client, MODEL = get_client()
os.makedirs("../reports", exist_ok=True)

USER_MODE = len(sys.argv) > 1 and sys.argv[1] == "user"

if USER_MODE:
    CSV_PATH = "../data/user_upload/test_questions.csv"
    OUT_CSV = "../reports/user_batch_result.csv"
    OUT_PDF = "../reports/User_Batch_Report.pdf"
else:
    CSV_PATH = "../data/test_questions.csv"
    OUT_CSV = "../reports/batch_test_result.csv"
    OUT_PDF = "../reports/LLM_Batch_Test_Report.pdf"

def get_ai_answer(question):
    try:
        resp = client.chat.completions.create(model=MODEL, messages=[{"role":"user","content":question}])
        return resp.choices[0].message.content.strip()
    except Exception as e:
        log(f"API Error: {e}", "ERROR")
        return f"API Error: {e}"

def score_answer(q, std, ans):
    try:
        prompt = f"""Evaluate: Score 1-5, Hallucination Yes/No, Accuracy, Comment.
Question: {q}
Standard: {std}
Answer: {ans}
"""
        resp = client.chat.completions.create(model=MODEL, messages=[{"role":"user","content":prompt}])
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"Score Error: {e}"

def extract_hallucination(text):
    try:
        match = re.search(r"Hallucination.*?(Yes|No)", text, re.I)
        return match.group(1) if match else "Unknown"
    except:
        return "Unknown"

def per_question_suggestion(score_text, has_hallucination):
    try:
        s = int(re.search(r"Score.*?(\d+)", score_text, re.I).group(1))
    except:
        s = 3
    if has_hallucination == "Yes":
        return "Hallucinated | Use RAG + strict grounding"
    elif s <= 2:
        return "Low quality | Improve prompt clarity"
    elif s <= 3:
        return "Moderate | Add more context"
    elif s <= 4:
        return "Good | Shorten answer"
    else:
        return "Excellent | Keep current logic"

def overall_suggestion(total, hal):
    if total == 0:
        return "No test results"
    rate = hal / total * 100
    if rate == 0:
        return "No hallucinations. Maintain current setup."
    elif rate <= 30:
        return "Mild hallucinations. Strengthen prompts."
    elif rate <= 70:
        return "Moderate risk. Use RAG for grounding."
    else:
        return "High risk. Add strict guardrails immediately."

def run_batch_test():
    if not os.path.exists(CSV_PATH):
        log(f"File missing: {CSV_PATH}", "ERROR")
        return
    try:
        df = pd.read_csv(CSV_PATH)
    except Exception as e:
        log(f"CSV read error: {e}", "ERROR")
        return

    total = len(df)
    hal_count = 0
    results = []

    log(f"Batch test started | Total: {total}")
    with Timer("Batch Test"):
        for i, row in df.iterrows():
            try:
                q = row["question"]
                std = row.get("standard_answer", "")
                ans = get_ai_answer(q)
                score = score_answer(q, std, ans)
                hal = extract_hallucination(score)
                if hal == "Yes":
                    hal_count += 1
                sugg = per_question_suggestion(score, hal)
                results.append({
                    "question": q,
                    "standard_answer": std,
                    "model_answer": ans,
                    "score": score,
                    "hallucination": hal,
                    "fix_suggestion": sugg
                })
                log(f"Done {i+1}/{total}")
            except Exception as e:
                log(f"Skip {i+1}: {e}", "WARN")

    try:
        pd.DataFrame(results).to_csv(OUT_CSV, index=False)
        accuracy = (total - hal_count)/total*100 if total>0 else 0
        generate_batch_pdf(total, hal_count, accuracy, OUT_PDF)
        plot_hallucination_pie(total, hal_count)
        log(f"Report saved: {OUT_CSV}")
    except Exception as e:
        log(f"Save failed: {e}", "ERROR")

    sugg = overall_suggestion(total, hal_count)
    log(f"FINAL | Hallucinations: {hal_count} | Accuracy: {accuracy:.1f}%")
    log(f"OVERALL: {sugg}")

if __name__ == "__main__":
    run_batch_test()