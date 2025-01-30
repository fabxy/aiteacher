# Calls OpenAI API for lesson generation
import openai
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def generate_lesson(user_level: str):
    prompt = f"Create a beginner-level SQL lesson about SELECT statements."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}],
        api_key=OPENAI_API_KEY
    )
    return response["choices"][0]["message"]["content"]
