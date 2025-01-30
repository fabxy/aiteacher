def test_register_user(client):
    response = client.post("/users/register/", json={"email": "test@example.com", "password": "securepassword"})
    assert response.status_code == 200
    assert response.json() == {"message": "User registered successfully!"}
