

def test_user_profile(client):

      # 1️⃣ Signup
    signup=client.post(
        "/api/v1/signup",
        json={
            "email": "test@example.com",
            "password": "secret123",
            "name": "Test User",
            "role": "student"
        },
    )
    print(signup.json())
      # 2️⃣ Login
    response = client.post(
        "/api/v1/login",
        data={"username": "test@example.com", "password": "secret123"},
    )
    print(response.json())
    assert response.status_code == 200
    token_data = response.json()

    access_token = token_data["access_token"]

    # 3️⃣ Call protected endpoint
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    print (response.json())   
    assert response.status_code == 200
 
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert data["is_active"] == True
    assert data["role"] == "student"
    assert data["name"] == "Test User"


def test_admin_user_profile(client):
    signup = client.post(
        "/api/v1/signup",
        json={
            "email": "admin@example.com",
            "password": "secret123",
            "name": "Admin User",
            "role": "admin",
        },
    )
    assert signup.status_code == 201

    response = client.post(
        "/api/v1/login",
        data={"username": "admin@example.com", "password": "secret123"},
    )
    assert response.status_code == 200
    token_data = response.json()

    access_token = token_data["access_token"]
    profile = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert profile.status_code == 200
    data = profile.json()
    assert data["email"] == "admin@example.com"
    assert data["role"] == "admin"

