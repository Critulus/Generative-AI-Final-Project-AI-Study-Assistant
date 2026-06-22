# AI Study Assistant

## Author

Christian Green
East Carolina University
Master of Science in Data Science

## Project Overview

The AI Study Assistant is a Generative AI application built using Python, Hugging Face Transformers, and Gradio. The application helps students study more effectively by generating:

* Summaries
* Key Takeaways
* Practice Questions
* Simple Explanations
* Flashcards

Users can either paste notes directly into the application or upload supported files such as PDF and text documents.

## Features

### Summary Generation

Creates a concise summary of the provided notes.

### Key Takeaways

Identifies the most important concepts and ideas.

### Practice Questions

Generates study questions to reinforce learning.

### Simple Explanation

Rewrites content in beginner-friendly language.

### Flashcard Creation

Automatically generates flashcards from the supplied material.

## Technologies Used

* Python
* Hugging Face Transformers
* Gradio
* PyTorch
* PyPDF

## Installation

Create a virtual environment:

```powershell
python -m venv hf-env
```

Activate the environment:

```powershell
.\hf-env\Scripts\Activate.ps1
```

Install required packages:

```powershell
pip install -r requirements.txt
```

## Running the Application

```powershell
python "Final Project AI Study Assistant.py"
```

The application will launch locally at:

```text
http://127.0.0.1:7860
```

## Future Enhancements

* Better instruction-tuned models
* PDF study guides
* Quiz generation with answer keys
* Export flashcards to Quizlet/Anki
* Multi-document support

## Learning Outcomes

This project provided experience with:

* Generative AI
* Hugging Face models
* Prompt engineering
* Python development
* Gradio web applications
* Local AI deployment

