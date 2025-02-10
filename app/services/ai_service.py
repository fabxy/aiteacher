# Calls OpenAI API for lesson generation
import openai
import os
import json
from dotenv import load_dotenv
from app.models import User, Lesson

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def generate_ai_lesson(user: User, lesson: Lesson):

    lesson_title = lesson.title.split("(")[0]
    lesson_duration = lesson.title.split("(")[1].split(")")[0]

    prompt = f"""
    Generate a structured SQL lesson on the topic {lesson_title} for a user with the following profile:    
    - SQL experience: {user.sql_experience}
    - Programming experience: {user.programming_experience}
    - Learning goals: {user.learning_goals}

    The lesson should take {lesson_duration} to complete and has to include: 
    - A brief introduction to the topic:
        - Explain the importance of the topic
        - Include use cases and applications
    - Multiple sections explaining theory and concepts of the topic:
        - Provide clear and structured explanations based on the users SQL experience
        - Relate concepts to the user's programming experience
        - Include multiple SQL examples illustrating the topic
        - Use sample datasets if needed
    - One practical exercise based on the lesson topic:
        - Define the problem statement clearly
        - Ask the user to write SQL code to solve the problem
        - Include sample input data and expected output

    Respond in markdown format. Here is an example of the expected format:
    # [Lesson title]
    ## Introduction
    ## [Section 1 title]
    ### [Subsection 1 title]
    ...
    ### [Subsection N title]
    ...
    ## [Section N title]
    ## Exercise
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
    - SQL experience: {user.sql_experience}
    - Programming experience: {user.programming_experience}
    - Learning goals: {user.learning_goals}
    - Time commitment: {user.learning_commitment}

    Write a list of lesson titles that allow the user to achieve their learning goals based on their SQL and programming experience.
    Specify the duration of each lesson, so that the overall duration adds up to the user's time commitment.

    Return a JSON list of lesson titles with the lesson duration in brackets, e.g.:
    ["Introduction to SQL (15 minutes)", "Filtering Data with WHERE (25 minutes)", "Joining Tables with JOIN (30 minutes)"]
    """
    
    client = openai.OpenAI(api_key=OPENAI_API_KEY)  # ✅ New OpenAI API format

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}]
    )

    lesson_titles = json.loads(response.choices[0].message.content)  # ✅ Extract response
    return lesson_titles