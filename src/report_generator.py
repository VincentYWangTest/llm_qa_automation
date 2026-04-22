from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import os

REPORTS_DIR = "../reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

def create_pdf(title, content_lines, output_path):
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph(title, styles["Heading1"]))
    story.append(Spacer(1, 20))
    for line in content_lines:
        story.append(Paragraph(line, styles["BodyText"]))
        story.append(Spacer(1, 6))
    doc.build(story)

def generate_batch_pdf(total, hallucination_count, accuracy, output_path):
    title = "LLM Hallucination Test Report"
    content = [
        f"Total Questions: {total}",
        f"Hallucination Count: {hallucination_count}",
        f"Model Accuracy: {accuracy:.1f}%",
        "",
        "Executive Summary:",
        "This report evaluates factual accuracy and hallucination risk.",
        "Higher accuracy means more reliable outputs.",
        "",
        "Recommendations:",
        "- Add strict grounding if hallucinations exist.",
        "- Use RAG to anchor answers in verified facts.",
        "- Run regular tests to maintain quality."
    ]
    create_pdf(title, content, output_path)

def generate_security_pdf(total, high_risk, output_path):
    title = "LLM Security Test Report"
    content = [
        f"Total Test Cases: {total}",
        f"High Risk Issues: {high_risk}",
        f"Low Risk Cases: {total - high_risk}",
        "",
        "Security Assessment:",
        "High risk indicates potential prompt leakage or weak guardrails.",
        "",
        "Recommendations:",
        "- Strengthen system prompt boundaries.",
        "- Add explicit refusal for injection attempts.",
        "- Block instruction override patterns."
    ]
    create_pdf(title, content, output_path)

def generate_rag_pdf(total, out_of_kb, output_path):
    title = "RAG Grounding Test Report"
    content = [
        f"Total Questions: {total}",
        f"Out-of-KB Answers: {out_of_kb}",
        f"Grounded Answers: {total - out_of_kb}",
        "",
        "RAG Performance Summary:",
        "Out-of-KB answers indicate poor context constraints.",
        "",
        "Optimization Tips:",
        "- Improve chunking and retrieval strategy.",
        "- Force LLM to use only provided knowledge.",
        "- Expand KB coverage for edge questions."
    ]
    create_pdf(title, content, output_path)