import datetime
import os
from utils import log

REPORTS_DIR = "../reports"

def generate_final_report(batch_total, hal_count, accuracy,
                          sec_total, high_risk,
                          rag_total, out_kb):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    md = f"""# LLM Full Test Summary Report
Generated at: {now}

## 1. Hallucination Test
- Total: {batch_total}
- Hallucinations: {hal_count}
- Accuracy: {accuracy:.1f}%

## 2. Security Test
- Total Cases: {sec_total}
- High Risk: {high_risk}

## 3. RAG Test
- Total Questions: {rag_total}
- Out-of-KB: {out_kb}

## Overall Recommendations
- Reduce hallucinations with prompt engineering and RAG.
- Fix high-risk security issues immediately.
- Improve knowledge base and retrieval for better RAG.

All detailed results: CSV / PDF / Charts / Logs
"""
    out_path = os.path.join(REPORTS_DIR, "final_test_report.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md)
    log("✅ Final report saved: final_test_report.md")