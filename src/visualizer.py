import matplotlib.pyplot as plt
import os

REPORTS_DIR = "../reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

def plot_hallucination_pie(total, hallucinations, path=f"{REPORTS_DIR}/hallucination_pie.png"):
    normal = total - hallucinations
    plt.figure(figsize=(6,6))
    plt.pie([normal, hallucinations], labels=["Normal","Hallucination"], 
            colors=["#66b3ff","#ff6666"], autopct="%1.1f%%")
    plt.title("Hallucination Distribution")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()

def plot_security_risk(high, low, path=f"{REPORTS_DIR}/security_risk.png"):
    plt.figure(figsize=(6,5))
    plt.bar(["High Risk","Low Risk"], [high, low], color=["#ff4444","#44aa44"])
    plt.title("Security Risk Distribution")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()

def plot_rag_out_of_kb(total, out_count, path=f"{REPORTS_DIR}/rag_out_of_kb.png"):
    in_count = total - out_count
    plt.figure(figsize=(6,6))
    plt.pie([in_count, out_count], labels=["In KB","Out of KB"],
            colors=["#55aa55","#ffaa33"], autopct="%1.1f%%")
    plt.title("RAG Answer Scope")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()