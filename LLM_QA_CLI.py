from dotenv import load_dotenv
import os
import re
from openai import OpenAI

# Load environment variables from .env
load_dotenv()

# Read API key
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Preprocessing
def preprocess_text(text):
    text = text.lower()                                  # lower-case
    text = re.sub(r"[^\w\s]", "", text)                  # remove punctuation
    tokens = text.split()                                # basic tokenization
    return " ".join(tokens)           
                   
# Sending questions to LLM

def ask_llm(question):
    prompt = f"Answer the following question clearly and simply:\n\n{question}\n"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

# Main CLI Loop

def main():
    print("Question Answering CLI Assistant")
    print("Type 'exit' to quit.\n")

    while True:
        user_question = input("Enter your question: ")

        if user_question.lower() == "exit":
            print("Goodbye!")
            break

        # Preprocess
        processed = preprocess_text(user_question)
        print("\nProcessed question:", processed)

        # Ask LLM
        answer = ask_llm(user_question)

        print("\nAnswer:", answer)
        print("\n" + "-"*50 + "\n")


if __name__ == "__main__":
    main()


