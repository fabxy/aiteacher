# Calls OpenAI API for lesson generation
import openai
import os
import json
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

def generate_curriculum(sql_experience, programming_experience, learning_commitment):
    prompt = f"""
    Create a personalized SQL learning curriculum for a user with the following profile:
    - SQL Experience: {sql_experience}
    - Programming Experience: {programming_experience}
    - Learning Commitment: {learning_commitment}

    Provide a JSON list of lesson titles like:
    ["Introduction to SQL", "Filtering Data with WHERE", "Joining Tables with JOIN"]
    """
    
    client = openai.OpenAI(api_key=OPENAI_API_KEY)  # ✅ New OpenAI API format

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}]
    )

    lesson_titles = json.loads(response.choices[0].message.content)  # ✅ Extract response
    return json.dumps(lesson_titles)