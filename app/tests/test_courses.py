def get_admin_token(client):
    # Signup
    client.post(
        "/api/v1/signup",
        json={
            "email": "admin@example.com",
            "password": "secret123",
            "name": "Admin User",
            "role": "admin",
        },
    )

    # Login
    response = client.post(
        "/api/v1/login",
        data={"username": "admin@example.com", "password": "secret123"},
    )

    return response.json()["access_token"]


# def create_admin_user(db)


def test_create_course(client):

    # Signup admin
    client.post(
        "/api/v1/signup",
        json={
            "email": "admin@example.com",
            "password": "secret123",
            "name": "Admin User",
            "role": "admin"
        },
    )

    # Login
    response = client.post(
        "/api/v1/login",
        data={"username": "admin@example.com", "password": "secret123"},
    )

    access_token = response.json()["access_token"]

    # Create course
    response = client.post(
        "/api/v1/create_course",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "title": "Math 101",
            "code": 101,
            "capacity": 10,
            "is_active": True
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert data["title"] == "Math 101"
    assert data["code"] == 101
    assert data["capacity"] == 10
    assert data["is_active"] is True
    assert "id" in data


def test_list_courses(client):

    client.post(
        "/api/v1/courses",
        json={
            "title": "Physics 101",
            "code": 102,
            "capacity": 20,
            "is_active": True,
        },
    )


    # 3️⃣ Call protected endpoint
    response = client.get(
        "/api/v1/all"
    )


    print (response.json())   
    assert response.status_code == 200
 
    data = response.json()
    assert len(data) > 0
    assert data[0]["title"] == "Physics 101"

def test_get_course_by_id(client):
    access_token = get_admin_token(client)

    create = client.post(
        "/api/v1/courses",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "title": "Chemistry",
            "code": 103,
            "capacity": 15,
            "is_active": True,
        },
    )

    course_id = create.json()["id"]

    # GET does NOT require auth
    response = client.get(f"/api/v1/courses/{course_id}")

    assert response.status_code == 200
    data = response.json()

    assert data["title"] == "Chemistry"

def test_get_course_by_id(client):
    access_token = get_admin_token(client)

    create = client.post(
        "/api/v1/courses",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "title": "Chemistry",
            "code": 103,
            "capacity": 15,
            "is_active": True,
        },
    )

    course_id = create.json()["id"]

    # GET does NOT require auth
    response = client.get(f"/api/v1/courses/{course_id}")

    assert response.status_code == 200
    data = response.json()

    assert data["title"] == "Chemistry"


def test_update_course(client):
    access_token = get_admin_token(client)

    create = client.post(
        "/api/v1/courses",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "title": "Biology",
            "code": 104,
            "capacity": 30,
            "is_active": True,
        },
    )

    course_id = create.json()["id"]

    response = client.put(
        f"/api/v1/courses/{course_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "title": "Advanced Biology",
            "code": 104,
            "capacity": 40,
            "is_active": True,
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert data["title"] == "Advanced Biology"
    assert data["capacity"] == 40


def test_activate_deactivate_course(client):
    access_token = get_admin_token(client)

    create = client.post(
        "/api/v1/courses",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "title": "History",
            "code": 105,
            "capacity": 25,
            "is_active": True,
        },
    )

    course_id = create.json()["id"]

    response = client.patch(
        f"/api/v1/courses/{course_id}/activate/false",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    data = response.json()

    assert data["is_active"] is False


# def test_update_course_by_id(client):
#       # 1️⃣ Signup
#     signup=client.post(
#         "/api/v1/signup",
#         json={
#             "email": "test@example.com",
#             "password": "secret123",
#             "name": "Test User",
#             "role": "admin"
#         },
#     )
#     print(signup.json())
#       # 2️⃣ Login
#     response = client.post(
#         "/api/v1/login",
#         data={"username": "test@example.com", "password": "secret123"},
#     )
#     print(response.json())
#     assert response.status_code == 200
#     token_data = response.json()

#     access_token = token_data["access_token"]
#     # 3️⃣ Call protected endpoint
#     response = client.put(
#         "/api/v1/create_course",
#         course_id = 1
#     )
#     print (response.json())   
#     assert response.status_code == 200
 
#     data = response.json()
#     assert data["title"] == "test@example.com"
#     assert data["code"] == 1
#     assert data["capacity"] == 10
#     assert data["is_active"] == True
#     assert data["id"] == 0


# def test_deactivate_course(client):
#       # 1️⃣ Signup
#     signup=client.post(
#         "/api/v1/signup",
#         json={
#             "email": "test@example.com",
#             "password": "secret123",
#             "name": "Test User",
#             "role": "admin"
#         },
#     )
#     print(signup.json())
#       # 2️⃣ Login
#     response = client.post(
#         "/api/v1/login",
#         data={"username": "test@example.com", "password": "secret123"},
#     )
#     print(response.json())
#     assert response.status_code == 200
#     token_data = response.json()

#     access_token = token_data["access_token"]
#     # 3️⃣ Call protected endpoint
#     response = client.patch(
#         "/api/v1/1/activate/true",
#         headers={"Authorization": f"Bearer {access_token}"},
#     )
#     print (response.json())   
#     assert response.status_code == 200
 
#     data = response.json()
#     assert data["title"] == "test@example.com"
#     assert data["code"] == 1
#     assert data["capacity"] == 10
#     assert data["is_active"] == True
#     assert data["id"] == 0