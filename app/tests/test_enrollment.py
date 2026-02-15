def test_enroll_course(client):

    # 1️⃣ Create admin
    client.post(
        "/api/v1/signup",
        json={
            "email": "admin@example.com",
            "password": "secret123",
            "name": "Admin User",
            "role": "admin"
        },
    )

    admin_login = client.post(
        "/api/v1/login",
        data={"username": "admin@example.com", "password": "secret123"},
    )

    admin_token = admin_login.json()["access_token"]

    # 2️⃣ Admin creates course
    course_response = client.post(
        "/api/v1/courses",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "title": "Math 101",
            "code": 101,
            "capacity": 10,
            "is_active": True,
        },
    )

    assert course_response.status_code == 200
    course_id = course_response.json()["id"]

    # 3️⃣ Create student
    client.post(
        "/api/v1/signup",
        json={
            "email": "student@example.com",
            "password": "secret123",
            "name": "Student User",
            "role": "student"
        },
    )

    student_login = client.post(
        "/api/v1/login",
        data={"username": "student@example.com", "password": "secret123"},
    )

    student_token = student_login.json()["access_token"]

    # 4️⃣ Student enrolls
    response = client.post(
        "/api/v1/enrollments",
        headers={"Authorization": f"Bearer {student_token}"},
        json={
            "course_id": course_id
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["course_id"] == course_id
    assert "id" in data
    assert "created_at" in data

def test_list_enrollments_admin(client):

    # Create admin
    client.post(
        "/api/v1/signup",
        json={
            "email": "admin@test.com",
            "password": "secret123",
            "name": "Admin",
            "role": "admin",
        },
    )

    admin_login = client.post(
        "/api/v1/login",
        data={"username": "admin@test.com", "password": "secret123"},
    )
    admin_token = admin_login.json()["access_token"]

    # Call endpoint (no enrollments yet)
    response = client.get(
        "/api/v1/enrollments",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_course_enrollments_admin(client):

    # Create admin
    client.post(
        "/api/v1/signup",
        json={
            "email": "admin2@test.com",
            "password": "secret123",
            "name": "Admin2",
            "role": "admin",
        },
    )

    admin_login = client.post(
        "/api/v1/login",
        data={"username": "admin2@test.com", "password": "secret123"},
    )
    admin_token = admin_login.json()["access_token"]

    # Create course
    course_response = client.post(
        "/api/v1/courses",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "title": "Physics",
            "code": 201,
            "capacity": 5,
            "is_active": True,
        },
    )

    course_id = course_response.json()["id"]

    # Call course enrollment list
    response = client.get(
        f"/api/v1/enrollments/course/{course_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    # Since no one enrolled yet, your service may return empty list
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_student_deregister(client):

    # Create admin
    client.post(
        "/api/v1/signup",
        json={
            "email": "admin3@test.com",
            "password": "secret123",
            "name": "Admin3",
            "role": "admin",
        },
    )

    admin_login = client.post(
        "/api/v1/login",
        data={"username": "admin3@test.com", "password": "secret123"},
    )
    admin_token = admin_login.json()["access_token"]

    # Create course
    course_response = client.post(
        "/api/v1/courses",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "title": "Biology",
            "code": 301,
            "capacity": 10,
            "is_active": True,
        },
    )

    course_id = course_response.json()["id"]

    # Create student
    client.post(
        "/api/v1/signup",
        json={
            "email": "student@test.com",
            "password": "secret123",
            "name": "Student",
            "role": "student",
        },
    )

    student_login = client.post(
        "/api/v1/login",
        data={"username": "student@test.com", "password": "secret123"},
    )
    student_token = student_login.json()["access_token"]

    # Enroll student
    enroll_response = client.post(
        "/api/v1/enrollments",
        headers={"Authorization": f"Bearer {student_token}"},
        json={"course_id": course_id},
    )

    assert enroll_response.status_code == 201

    # Deregister
    response = client.delete(
        f"/api/v1/enrollments/{course_id}",
        headers={"Authorization": f"Bearer {student_token}"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Successfully deregistered"
