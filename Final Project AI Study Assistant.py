# Final Project: AI Study Assistant

import os
import gradio as gr
import random
from transformers import pipeline
from pypdf import PdfReader

hf_token = os.getenv("HF_TOKEN")

generator = pipeline(
    "text-generation",
    model="distilgpt2",
    token=hf_token
)


def read_uploaded_file(file):
    if file is None:
        return ""

    file_path = file.name

    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        text = " ".join(text.split())
        return text[:1500]

    if file_path.endswith(".txt") or file_path.endswith(".md"):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        text = " ".join(text.split())
        return text[:1500]

    return ""


def generate_response(prompt, max_tokens=120):
    result = generator(
        prompt,
        max_new_tokens=max_tokens,
        do_sample=True,
        temperature=0.8,
        top_p=0.9,
        repetition_penalty=1.2,
        pad_token_id=generator.tokenizer.eos_token_id,
    )

    generated_text = result[0]["generated_text"]
    return generated_text.replace(prompt, "").strip()


def generate_flashcards(notes):
    flashcards = []

    # Split notes into chunks using periods and line breaks
    raw_chunks = notes.replace("\n", ". ").split(".")

    clean_chunks = []

    for chunk in raw_chunks:
        chunk = chunk.strip()

        if len(chunk) > 30:
            clean_chunks.append(chunk)

    if not clean_chunks:
        return "Not enough content was provided to create flashcards."

    question_formats = [
        "What is the main idea of this statement?",
        "Why is this concept important?",
        "How would you explain this concept on a test?",
        "What should a student remember about this topic?",
        "How does this idea connect to the broader lesson?",
        "What is the significance of this information?",
        "What does this concept help explain?",
        "How could this concept be applied?"
    ]

    flashcards_text = ""

    for i, chunk in enumerate(clean_chunks[:8]):
        question = question_formats[i % len(question_formats)]

        flashcards_text += f"Question {i + 1}: {question}\n"
        flashcards_text += f"Answer {i + 1}: {chunk}.\n\n"

    return flashcards_text.strip()


def get_clean_chunks(notes):
    raw_chunks = notes.replace("\n", ". ").split(".")
    clean_chunks = []

    for chunk in raw_chunks:
        chunk = chunk.strip()

        if len(chunk) > 30:
            clean_chunks.append(chunk)

    return clean_chunks


def generate_key_takeaways(notes):
    chunks = get_clean_chunks(notes)

    if not chunks:
        return "Not enough content was provided to generate key takeaways."

    output = ""

    for i, chunk in enumerate(chunks[:5]):
        output += f"{i + 1}. {chunk}.\n"

    return output.strip()


def generate_practice_questions(notes):
    chunks = get_clean_chunks(notes)

    if not chunks:
        return "Not enough content was provided to generate practice questions."

    question_formats = [
        "What is the main idea of this concept?",
        "Why is this concept important?",
        "How would you explain this on a test?",
        "What should students remember about this topic?",
        "How does this idea connect to the broader lesson?"
    ]

    output = ""

    for i, chunk in enumerate(chunks[:5]):
        output += f"{i + 1}. {question_formats[i]}\n"
        output += f"   Suggested Answer: {chunk}.\n\n"

    return output.strip()


def generate_simple_explanation(notes):
    chunks = get_clean_chunks(notes)

    if not chunks:
        return "Not enough content was provided to generate a simple explanation."

    return "In simple terms: " + " ".join(chunks[:3]) + "."

def ai_study_helper(notes, uploaded_file):
    file_text = read_uploaded_file(uploaded_file)

    combined_notes = f"{notes}\n\n{file_text}".strip()
    combined_notes = combined_notes[:1500]

    if not combined_notes:
        return (
            "Please enter notes or upload a file.",
            "",
            "",
            "",
            ""
        )

    summary_prompt = f"""
You are a study assistant.

Summarize the following notes in 3-5 sentences.

Notes:
{combined_notes}

Summary:
"""

    # AI-generated summary
    summary = generate_response(summary_prompt, 120)

    # Rule-based study materials
    key_points = generate_key_takeaways(combined_notes)
    questions = generate_practice_questions(combined_notes)
    simple_explanation = generate_simple_explanation(combined_notes)
    flashcards = generate_flashcards(combined_notes)

    return (
        summary,
        key_points,
        questions,
        simple_explanation,
        flashcards
    )


demo = gr.Interface(
    fn=ai_study_helper,

    inputs=[
        gr.Textbox(
            lines=12,
            label="📚 Paste Your Class Notes"
        ),
        gr.File(
            label="📄 Optional: Upload Notes File",
            file_types=[".txt", ".md", ".pdf"]
        )
    ],

    outputs=[
        gr.Textbox(label="📝 Summary"),
        gr.Textbox(label="⭐ Key Takeaways"),
        gr.Textbox(label="❓ Practice Questions"),
        gr.Textbox(label="💡 Simple Explanation"),
        gr.Textbox(label="🃏 Flashcards"),
    ],

    title="📚 AI Study Assistant",

    description="""
## Generative AI Project

**Christian Green**  
East Carolina University  
M.S. Data Science  

This application uses a Hugging Face generative AI model to help students study class material.

The AI Study Assistant can generate:
- Summaries
- Key takeaways
- Practice questions
- Simplified explanations
- Flashcards

Built using:
- Hugging Face Transformers
- Python
- Gradio
- PyPDF
""",

    examples=[
        [
            "The attention mechanism allows transformer models to dynamically focus on relevant words in a sequence, improving contextual understanding and language modeling.",
            None
        ],
        [
            "Machine learning is a type of artificial intelligence that allows computers to learn patterns from data. Supervised learning uses labeled examples, while unsupervised learning finds patterns without labels.",
            None
        ],
    ],
)

demo.launch()
