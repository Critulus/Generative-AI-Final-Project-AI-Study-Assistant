# AI Study Assistant

## Author

**Christian Green**
East Carolina University
Master of Science in Data Science

---

## Project Overview

The AI Study Assistant is a Generative AI application built using Python, Hugging Face Transformers, and Gradio. The application helps students study course materials by automatically generating summaries, key takeaways, practice questions, simplified explanations, and flashcards from class notes or uploaded documents.

This project demonstrates the practical application of Generative AI to educational content by transforming lecture notes into useful study resources.

---

## Features

The AI Study Assistant can:

* Generate AI-powered summaries of class notes
* Extract important key takeaways
* Create practice questions for exam preparation
* Generate simplified explanations for beginners
* Create flashcards for studying and review
* Accept pasted text notes
* Process uploaded PDF files
* Process uploaded TXT and Markdown files

---

## Technology Stack

### Programming Language

* Python

### Libraries and Frameworks

* Gradio
* Hugging Face Transformers
* DistilGPT2
* PyPDF

### AI Model

* DistilGPT2 (Hugging Face)

---

## How It Works

1. The user enters class notes or uploads a supported document.
2. The application extracts and processes the text.
3. DistilGPT2 generates a summary of the material.
4. Additional study tools generate:

   * Key Takeaways
   * Practice Questions
   * Simple Explanations
   * Flashcards
5. Results are displayed in the Gradio interface.

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/Critulus/Generative-AI-Final-Project-AI-Study-Assistant.git
cd Generative-AI-Final-Project-AI-Study-Assistant
```

### Create a Virtual Environment

```bash
python -m venv hf-env
```

### Activate the Virtual Environment

Windows:

```bash
hf-env\Scripts\activate
```

Mac/Linux:

```bash
source hf-env/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

Start the application:

```bash
python "Final Project AI Study Assistant.py"
```

After launching, Gradio will provide a local URL similar to:

```text
http://127.0.0.1:7860
```

Open the URL in a web browser to use the application.

---

## Example Workflow

### Input

```text
Machine learning is a type of artificial intelligence that allows computers to learn patterns from data. Supervised learning uses labeled examples, while unsupervised learning finds patterns without labels.
```

### Output

**Summary**

* Brief overview of the material.

**Key Takeaways**

* Important concepts extracted from the notes.

**Practice Questions**

* Exam-style review questions.

**Simple Explanation**

* Beginner-friendly explanation of the topic.

**Flashcards**

* Question and answer study cards.

---

## Project Structure

```text
Generative-AI-Final-Project-AI-Study-Assistant/
│
├── Final Project AI Study Assistant.py
├── README.md
├── requirements.txt
├── .gitignore
│
└── docs/
    └── AI_Study_Assistant_Project_Documentation.docx
```

---

## Known Limitations

* DistilGPT2 is a lightweight language model and may occasionally generate inaccurate summaries.
* PDF extraction quality depends on document formatting.
* Flashcards are generated from extracted content and may require user review.
* Results should be used as study aids rather than replacements for course materials.

---

## Future Improvements

Potential future enhancements include:

* Support for larger language models
* Better PDF parsing and formatting preservation
* Export study materials to PDF
* Quiz generation with scoring
* Support for PowerPoint and Word documents
* AI-generated study plans

---

## Educational Purpose

This project was developed as part of the Generative AI course within the East Carolina University Master of Science in Data Science program. The objective was to demonstrate the application of Generative AI techniques to solve a real-world educational problem.

---
