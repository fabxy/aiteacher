def test_execute_sql(client):
    response = client.post("/sql/run/", json={"query": "SELECT 1;"})
    assert response.status_code == 200, response.text
    assert "result" in response.json()