# Calls OpenAI API for lesson generation
import openai
import os
import json
from dotenv import load_dotenv
from app.models import User, Lesson

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def generate_ai_curriculum(user: User):
    prompt = f"""
    Create a personalized SQL learning curriculum for a user with the following profile:
    - SQL experience: {user.sql_experience}
    - Programming experience: {user.programming_experience}
    - Learning goals: {user.learning_goals}
    - Preferred number of lessons: {user.learning_commitment}

    Write a list of lesson titles that allow the user to achieve their learning goals based on their SQL and programming experience.
    Ensure that the length of the list matches the user's preferred number of lessons.
    Return the list of lesson titles in JSON format, e.g.:
    ["Introduction to SQL", "Filtering Data with WHERE", "Joining Tables with JOIN"]
    """

    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}]
    )

    lesson_titles = json.loads(response.choices[0].message.content)
    return lesson_titles


def generate_ai_lesson(user: User, lesson: Lesson, completed_lessons: list[str]):

    if completed_lessons:
        previous_lessons_text = f"""
        The user has already completed lessons with the following titles:
        - {'\n\t- '.join([cl.title for cl in completed_lessons])}
        """
        previous_lessons_text += f"""
        The following is the content of the last lesson: 
        [START LAST LESSON]
        {completed_lessons[-1].content}
        [END LAST LESSON]
        """
    else:
        previous_lessons_text = """
        It is the user's first lesson of this course.
        """

    prompt = f"""
    Generate a structured SQL lesson on the topic {lesson.title} for a user with the following profile:    
    - SQL experience: {user.sql_experience}
    - Programming experience: {user.programming_experience}
    - Learning goals: {user.learning_goals}

    {previous_lessons_text}

    The new lesson on {lesson.title} should be tailored to the user's SQL and programming experience and learning goals. 
    The lesson should have the following structure:
    - A brief introduction to the topic:
        - Explain the importance of the topic
        - Include use cases and applications
    - Multiple sections explaining theory and concepts of the topic:
        - Provide clear and structured explanations based on the user's SQL experience
        - Relate concepts to the user's programming experience
        - Include multiple SQL examples illustrating the topic
    - One practical exercise based on the lesson topic:
        - Define the problem statement clearly
        - Include sample input data
        - Ask the user to write SQL code to solve the problem

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

    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}]
    )

    return response.choices[0].message.content


def generate_ai_data(lesson: Lesson):

    prompt=f"""Write a SQL query to create the sample data of the exercise of the following lesson:
    {lesson.content}
    
    Return only the SQL query that creates the table and inserts the sample data into the table.
    Respond in the following JSON format:
    {{
        "queries": ["SQL query 1", "SQL query 2", ...],
    }}
    """

    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}]
    )

    return response.choices[0].message.content