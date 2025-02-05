# Calls OpenAI API for lesson generation
import openai
import os
import json
from dotenv import load_dotenv
from app.models import User, Lesson

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def generate_ai_lesson(user: User, lesson: Lesson):
    prompt = f"""
    Create a personalized SQL lesson on the topic:
    - {lesson.title} 
    
    for a user with the following profile:
    - SQL Experience: {user.sql_experience}
    - Programming Experience: {user.programming_experience}
    - Learning Commitment: {user.learning_commitment}

    The lesson should include: 
    - A brief introduction to the topic
    - Multiple sections explaining theory and concepts with examples
    - One exercise to which the user is promted to code the answer.

    Respond in markdown format.
    """
    
    client = openai.OpenAI(api_key=OPENAI_API_KEY)  # ✅ New OpenAI API format

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}]
    )

    return response.choices[0].message.content

def generate_ai_curriculum(user: User):
    prompt = f"""
    Create a personalized SQL learning curriculum for a user with the following profile:
    - SQL Experience: {user.sql_experience}
    - Programming Experience: {user.programming_experience}
    - Learning Commitment: {user.learning_commitment}

    Provide a JSON list of lesson titles like:
    ["Introduction to SQL", "Filtering Data with WHERE", "Joining Tables with JOIN"]
    """
    
    client = openai.OpenAI(api_key=OPENAI_API_KEY)  # ✅ New OpenAI API format

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}]
    )

    lesson_titles = json.loads(response.choices[0].message.content)  # ✅ Extract response
    return lesson_titles