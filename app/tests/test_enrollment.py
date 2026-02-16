def create_admin_and_get_token(client):
    client.post(
        "/api/v1/signup",
        json={
            "email": "admin@example.com",
            "password": "secret123",
            "name": "Admin User",
            "role": "admin",
        },
    )

    response = client.post(
        "/api/v1/login",
        data={"username": "admin@example.com", "password": "secret123"},
    )

    return response.json()["access_token"]


def create_student_and_get_token(client):
    client.post(
        "/api/v1/signup",
        json={
            "email": "student@example.com",
            "password": "secret123",
            "name": "Student User",
            "role": "student",
        },
    )

    response = client.post(
        "/api/v1/login",
        data={"username": "student@example.com", "password": "secret123"},
    )

    return response.json()["access_token"]

def create_course(client, admin_token):
    response = client.post(
        "/api/v1/courses",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "title": "Test Course",
            "code": 999,
            "capacity": 10,
            "is_active": True,
        },
    )

    return response.json()["id"]

def test_student_enroll(client):
    admin_token = create_admin_and_get_token(client)
    student_token = create_student_and_get_token(client)

    course_id = create_course(client, admin_token)

    response = client.post(
        "/api/v1/enrollments",
        headers={"Authorization": f"Bearer {student_token}"},
        json={"course_id": course_id},
    )

    assert response.status_code == 201
    data = response.json()

    assert data["course_id"] == course_id
    assert "id" in data

def test_student_cannot_enroll_twice(client):
    admin_token = create_admin_and_get_token(client)
    student_token = create_student_and_get_token(client)

    course_id = create_course(client, admin_token)

    client.post(
        "/api/v1/enrollments",
        headers={"Authorization": f"Bearer {student_token}"},
        json={"course_id": course_id},
    )

    response = client.post(
        "/api/v1/enrollments",
        headers={"Authorization": f"Bearer {student_token}"},
        json={"course_id": course_id},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Already enrolled"

def test_admin_list_enrollments(client):
    admin_token = create_admin_and_get_token(client)
    student_token = create_student_and_get_token(client)

    course_id = create_course(client, admin_token)

    client.post(
        "/api/v1/enrollments",
        headers={"Authorization": f"Bearer {student_token}"},
        json={"course_id": course_id},
    )

    response = client.get(
        "/api/v1/enrollments",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 200
    assert len(response.json()) > 0

def test_admin_view_enrollments_by_course(client):
    admin_token = create_admin_and_get_token(client)
    student_token = create_student_and_get_token(client)

    course_id = create_course(client, admin_token)

    client.post(
        "/api/v1/enrollments",
        headers={"Authorization": f"Bearer {student_token}"},
        json={"course_id": course_id},
    )

    response = client.get(
        f"/api/v1/enrollments/by-course/{course_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["course_id"] == course_id

def test_student_deregister(client):
    admin_token = create_admin_and_get_token(client)
    student_token = create_student_and_get_token(client)

    course_id = create_course(client, admin_token)

    client.post(
        "/api/v1/enrollments",
        headers={"Authorization": f"Bearer {student_token}"},
        json={"course_id": course_id},
    )

    response = client.delete(
        f"/api/v1/enrollments/course/{course_id}",
        headers={"Authorization": f"Bearer {student_token}"},
    )

    assert response.status_code == 204

def test_student_cannot_deregister_without_enrollment(client):
    admin_token = create_admin_and_get_token(client)
    student_token = create_student_and_get_token(client)

    course_id = create_course(client, admin_token)

    response = client.delete(
        f"/api/v1/enrollments/course/{course_id}",
        headers={"Authorization": f"Bearer {student_token}"},
    )

    assert response.status_code == 400
    assert "Not Registered" in response.json()["detail"]
