# -*- coding: utf-8 -*-
"""Untitled4.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1IE-9SJuxbDooyFbzQkavKfuy3dkLqE9H
"""

# Install required packages
!pip install groq python-dotenv gradio -q

# Import necessary libraries
from groq import Groq
import gradio as gr
import os

# Define the GROQ API key directly in the code (replace with your actual key)
GROQ_API_KEY = "your_groq_api_key_here"  # Replace this with your actual GROQ API key from GroqCloud

# Initialize GROQ client with the defined API key
client = Groq(api_key=GROQ_API_KEY)

def generate_documentation(code_input):
    """Generate documentation using GROQ API."""
    if not code_input.strip():
        return "Error: No code provided for documentation."

    # Prepare the prompt for GROQ
    prompt = (
        f"Generate a detailed documentation or overview for the following code. "
        f"Explain its purpose, structure, and functionality. Include comments on potential improvements if applicable. "
        f"Code:\n{code_input}"
    )

    try:
        # Call GROQ API for chat completion
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful code documentation assistant."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile",  # Use a suitable GROQ model
            max_completion_tokens=2048,      # Adjust based on needs
            temperature=0.2                  # Lower temperature for more deterministic output
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating documentation: {str(e)}"

def save_and_display_documentation(doc_text):
    """Save documentation to a file and return it for display."""
    filename = "/content/output/documentation.md"
    # Create output directory if it doesn't exist
    !mkdir -p /content/output
    with open(filename, 'w') as file:
        file.write(doc_text)
    print(f"Documentation saved to {filename}")
    # Provide a download link for the file
    from google.colab import files
    files.download(filename)
    return doc_text

def process_input(code_input, uploaded_file):
    """Process the input code (from textbox or uploaded file) and return documentation."""
    if uploaded_file:
        code_input = uploaded_file.decode("utf-8")  # Decode file content
    if not code_input:
        return "Please provide code or upload a file."
    documentation = generate_documentation(code_input)
    return save_and_display_documentation(documentation)

# Create Gradio interface
interface = gr.Interface(
    fn=process_input,
    inputs=[
        gr.Textbox(lines=10, label="Enter your code here", placeholder="Type or paste your code..."),
        gr.File(label="Or upload a .py file", file_types=[".py"])
    ],
    outputs=gr.Textbox(label="Generated Documentation", lines=20),
    title="Code Documentation Generator",
    description="Enter code or upload a .py file to generate detailed documentation using the GROQ API.",
    examples=[
        ["def add(a, b):\n    return a + b\nprint(add(2, 3))"],
        # Note: File example path needs to be adjusted after upload (e.g., "/content/uploaded_file.py")
    ]
)

# Launch the interface
interface.launch()