import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")


def get_feedback(question, answer):

    prompt = f"""
You are an AI viva examiner.

Question:
{question}

Student Answer:
{answer}

Evaluate the student's answer.

Give the response in this format:

Score: X/10

Correct Points:
- point 1
- point 2

Mistakes:
- mistake 1
- mistake 2

Suggestions:
- suggestion 1
- suggestion 2

Model Answer:
Give a short correct answer.
"""

    url = "https://generativelanguage.googleapis.com/v1beta/interactions"

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": API_KEY
    }

    data = {
        "model": "gemini-3.5-flash-lite",
        "input": prompt
    }

    response = requests.post(
        url,
        headers=headers,
        json=data
    )

    if response.status_code != 200:
        return f"Error: {response.text}"

    result = response.json()

    # Get Gemini's generated text
    try:
        feedback = result["steps"][-1]["content"][0]["text"]
        return feedback
    except (KeyError, IndexError, TypeError):
        return "Could not read Gemini's response."

