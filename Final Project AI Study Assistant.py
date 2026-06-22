# Final Project: AI Study Assistant

import os
import gradio as gr
from transformers import pipeline
from pypdf import PdfReader

# Optional Hugging Face token
hf_token = os.getenv("HF_TOKEN")

# Load Hugging Face model
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
                text += page_text.replace("\n", " ")

        text = " ".join(text.split())
        text = text[:1500]

        return text

    if file_path.endswith(".txt") or file_path.endswith(".md"):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        text = " ".join(text.split())
        text = text[:1500]

        return text

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
    sentences = notes.split(".")
    clean_sentences = []

    for sentence in sentences:
        sentence = sentence.strip()

        if len(sentence) > 25:
            clean_sentences.append(sentence)

    if not clean_sentences:
        return "Not enough content was provided to create flashcards."

    flashcards = ""

    for i, sentence in enumerate(clean_sentences[:5]):
        flashcards += f"Question {i + 1}: What is one important concept from the notes?\n"
        flashcards += f"Answer {i + 1}: {sentence}.\n\n"

    return flashcards.strip()


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

    key_points_prompt = f"""
You are a study assistant.

List 5 key takeaways from these notes.

Notes:
{combined_notes}

Key Takeaways:
"""

    questions_prompt = f"""
You are a study assistant.

Create 3 practice questions based on these notes.

Notes:
{combined_notes}

Practice Questions:
"""

    simple_prompt = f"""
You are a study assistant.

Explain these notes as if teaching a beginner.

Notes:
{combined_notes}

Simple Explanation:
"""

    summary = generate_response(summary_prompt, 120)
    key_points = generate_response(key_points_prompt, 120)
    questions = generate_response(questions_prompt, 120)
    simple_explanation = generate_response(simple_prompt, 140)
    flashcards = generate_flashcards(combined_notes)

    return summary, key_points, questions, simple_explanation, flashcards


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
