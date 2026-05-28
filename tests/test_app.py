from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_get_root_redirects_to_static_index():
    # Arrange
    path = "/"

    # Act
    response = client.get(path, follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_activity_list():
    # Arrange
    path = "/activities"

    # Act
    response = client.get(path)

    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert "Chess Club" in activities
    assert activities["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"


def test_signup_for_activity_succeeds_for_valid_signup():
    # Arrange
    path = "/activities/Programming Class/signup"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(path, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Programming Class"}
    participants = client.get("/activities").json()["Programming Class"]["participants"]
    assert email in participants


def test_signup_for_activity_returns_400_for_duplicate_signup():
    # Arrange
    path = "/activities/Chess Club/signup"
    email = "michael@mergington.edu"

    # Act
    response = client.post(path, params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_for_activity_returns_404_for_missing_activity():
    # Arrange
    path = "/activities/Nonexistent/signup"
    email = "student@mergington.edu"

    # Act
    response = client.post(path, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_participant_succeeds_for_existing_participant():
    # Arrange
    path = "/activities/Basketball Team/participants"
    email = "alex@mergington.edu"

    # Act
    response = client.delete(path, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from Basketball Team"}
    participants = client.get("/activities").json()["Basketball Team"]["participants"]
    assert email not in participants


def test_remove_participant_returns_400_for_missing_participant():
    # Arrange
    path = "/activities/Basketball Team/participants"
    email = "missing@mergington.edu"

    # Act
    response = client.delete(path, params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Participant not found for this activity"


def test_remove_participant_returns_404_for_missing_activity():
    # Arrange
    path = "/activities/Nonexistent/participants"
    email = "student@mergington.edu"

    # Act
    response = client.delete(path, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
