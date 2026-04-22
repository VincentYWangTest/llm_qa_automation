import pandas as pd
import os
import sys
from config import get_client
from report_generator import generate_rag_pdf
from visualizer import plot_rag_out_of_kb
from utils import log, Timer

client, MODEL = get_client()
os.makedirs("../reports", exist_ok=True)

USER_MODE = len(sys.argv) > 1 and sys.argv[1] == "user"

if USER_MODE:
    KB_PATH = "../data/user_upload/knowledge.txt"
    Q_PATH = "../data/user_upload/rag_questions.csv"
    OUT_CSV = "../reports/user_rag_result.csv"
    OUT_PDF = "../reports/User_RAG_Report.pdf"
else:
    KB_PATH = "../data/knowledge.txt"
    Q_PATH = "../data/rag_questions.csv"
    OUT_CSV = "../reports/rag_test_result.csv"
    OUT_PDF = "../reports/LLM_RAG_Report.pdf"

def load_kb():
    try:
        with open(KB_PATH,"r",encoding="utf-8") as f:
            return f.read()
    except:
        return ""

def answer(q, kb):
    try:
        prompt = f"Use ONLY this knowledge:\n{kb}\nQuestion: {q}\nAnswer:"
        resp = client.chat.completions.create(model=MODEL, messages=[{"role":"user","content":prompt}])
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

def is_out_of_kb(q, ans, kb):
    try:
        prompt = f"Does answer use info outside KB? Yes/No\nKB:{kb}\nQ:{q}\nAns:{ans}\nOut:"
        resp = client.chat.completions.create(model=MODEL, messages=[{"role":"user","content":prompt}])
        return "yes" in resp.choices[0].message.content.strip().lower()
    except:
        return False

def rag_suggestion(ans, oob):
    if "Error" in ans:
        return "API error"
    elif oob:
        return "OUT OF KB | Strengthen constraints"
    elif len(ans)>120:
        return "Too long | Shorten answer"
    else:
        return "Good | Properly grounded"

def run_rag_test():
    if not os.path.exists(Q_PATH):
        log(f"Missing questions: {Q_PATH}", "ERROR")
        return
    try:
        df = pd.read_csv(Q_PATH)
    except Exception as e:
        log(f"CSV error: {e}", "ERROR")
        return
    kb = load_kb()
    results = []
    log(f"RAG test | Questions: {len(df)}")
    with Timer("RAG Test"):
        for i, row in df.iterrows():
            try:
                q = row["question"]
                ans = answer(q, kb)
                oob = is_out_of_kb(q, ans, kb)
                sugg = rag_suggestion(ans, oob)
                results.append({"question":q,"answer":ans,"out_of_kb":oob,"fix_suggestion":sugg})
                log(f"Done {i+1}/{len(df)}")
            except Exception as e:
                log(f"Skip {i+1}: {e}", "WARN")
    try:
        pd.DataFrame(results).to_csv(OUT_CSV, index=False)
        out_count = sum(1 for r in results if r["out_of_kb"])
        generate_rag_pdf(len(df), out_count, OUT_PDF)
        plot_rag_out_of_kb(len(df), out_count)
        log(f"RAG report saved | Out-of-KB: {out_count}")
    except Exception as e:
        log(f"Save failed: {e}", "ERROR")

if __name__ == "__main__":
    run_rag_test()