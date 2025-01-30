def test_create_lesson(client):
    lesson_data = {"title": "Introduction to SQL", "content": "Learn about SELECT statements."}
    response = client.post("/lessons/", json=lesson_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Introduction to SQL"

def test_get_lessons(client):
    response = client.get("/lessons/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
