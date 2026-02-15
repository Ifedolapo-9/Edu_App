from app.core.security import verify_password

def test_signup_and_login(client):
    #Signup
    response = client.post(
        "/api/v1/signup",
        json={
            "email": "test@example.com",
            "password": "secret123",
            "name": "Test User",
            "role": "student"
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "User created successfully"
    assert data["username"] == "Test User"


    #Login 

    response = client.post(
        "/api/v1/login",
        data={"username": "test@example.com", "password": "secret123"},
    )
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"


def test_login_invalid_credentials(client):
    #Attempt login with invalid credentials
    response = client.post(
        "/api/v1/login",
        data={"username":"test@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 400