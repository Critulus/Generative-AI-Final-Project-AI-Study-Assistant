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
            text += page.extract_text() or ""
        return text

    if file_path.endswith(".txt") or file_path.endswith(".md"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

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

def ai_study_helper(notes, uploaded_file):
    file_text = read_uploaded_file(uploaded_file)

    combined_notes = f"{notes}\n\n{file_text}".strip()

    if not combined_notes:
        return (
            "Please enter notes or upload a file.",
            "",
            "",
            "",
            ""
        )

    summary_prompt = f"""
Summarize the following class notes in a short paragraph:

{combined_notes}

Summary:
"""

    key_points_prompt = f"""
List the most important key takeaways from these class notes:

{combined_notes}

Key Takeaways:
"""

    questions_prompt = f"""
Create three practice questions based on these class notes:

{combined_notes}

Practice Questions:
"""

    simple_prompt = f"""
Explain this topic in very simple language for a beginner:

{combined_notes}

Simple Explanation:
"""

    flashcard_prompt = f"""
Create five flashcards from these class notes.
Format each flashcard as Question: and Answer:

{combined_notes}

Flashcards:
"""

    summary = generate_response(summary_prompt, 120)
    key_points = generate_response(key_points_prompt, 120)
    questions = generate_response(questions_prompt, 120)
    simple_explanation = generate_response(simple_prompt, 140)
    flashcards = generate_response(flashcard_prompt, 160)

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
            "Neural networks learn patterns by adjusting weights during training using backpropagation and gradient descent.",
            None
        ],
    ],
)

demo.launch()
