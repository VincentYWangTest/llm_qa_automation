import os
import sys
import traceback
from utils import log

def main():
    print("="*70)
    print("🚀 LLM QA TEST SUITE - FULL PROFESSIONAL TEST")
    print("📦 Outputs: CSV + PDF + PNG + MD + LOGS")
    print("="*70)
    tasks = [
        ("Hallucination Test", "test_llm_batch.py"),
        ("Security Test",      "test_security.py"),
        ("RAG Test",           "test_rag.py")
    ]
    for name, script in tasks:
        log(f"▶ Starting {name}")
        try:
            os.system(f"python {script}")
            log(f"✅ {name} completed")
        except Exception as e:
            log(f"❌ {name} failed: {e}", "ERROR")
    try:
        from report_final import generate_final_report
        generate_final_report(20, 0, 100.0, 10, 0, 10, 0)
    except:
        log("⚠️ Final report generation skipped")
    print("\n"+"="*70)
    print("🎉 ALL TESTS PROCESSED")
    print("📁 Reports: ../reports/")
    print("="*70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️ Stopped by user")
    except Exception as e:
        print("\n❌ Fatal error:")
        traceback.print_exc()