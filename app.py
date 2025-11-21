from flask import Flask, render_template, request
from dotenv import load_dotenv
from openai import OpenAI
import os
import re

# Load API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

app = Flask(__name__)

# Preprocessing function
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    tokens = text.split()
    return " ".join(tokens)

# LLM function
def ask_llm(question):
    prompt = f"Answer the following question clearly:\n\n{question}\n"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

# Web route
@app.route("/", methods=["GET", "POST"])
def home():
    answer = ""
    processed = ""
    question = ""

    if request.method == "POST":
        question = request.form["question"]
        processed = preprocess_text(question)
        answer = ask_llm(question)

    return render_template(
        "index.html",
        question=question,
        processed=processed,
        answer=answer
    )

if __name__ == "__main__":
    app.run(debug=True)
