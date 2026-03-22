import pytest


def test_signup_success(test_client, reset_activities):
    """Test successful signup for an activity"""
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    
    # Act
    response = test_client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    assert "Signed up" in data["message"]
    assert email in data["message"]


def test_signup_adds_participant(test_client, reset_activities):
    """Test that signup actually adds participant to list"""
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    
    # Act
    test_client.post(f"/activities/{activity_name}/signup?email={email}")
    response = test_client.get("/activities")
    participants = response.json()[activity_name]["participants"]
    
    # Assert
    assert email in participants


def test_signup_nonexistent_activity(test_client, reset_activities):
    """Test signup for non-existent activity"""
    # Arrange
    nonexistent_activity = "Fake Activity"
    email = "student@mergington.edu"
    
    # Act
    response = test_client.post(
        f"/activities/{nonexistent_activity}/signup?email={email}"
    )
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_already_registered(test_client, reset_activities):
    """Test signup when student is already registered"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already registered in fixture
    
    # Act
    response = test_client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_activity_full(test_client, reset_activities):
    """Test signup when activity is full"""
    # Arrange
    email = "newstudent@mergington.edu"
    activities_data = test_client.get("/activities").json()
    
    # Find an activity that's full
    full_activity = None
    for activity_name, activity_data in activities_data.items():
        if len(activity_data["participants"]) >= activity_data["max_participants"]:
            full_activity = activity_name
            break
    
    # Act
    response = test_client.post(
        f"/activities/{full_activity}/signup?email={email}"
    )
    
    # Assert
    assert response.status_code == 400
    assert "Activity is full" in response.json()["detail"]


def test_signup_multiple_emails_to_same_activity(test_client, reset_activities):
    """Test signing up multiple different students to same activity"""
    # Arrange
    activity_name = "Chess Club"
    email1 = "student1@mergington.edu"
    email2 = "student2@mergington.edu"
    
    # Act
    test_client.post(f"/activities/{activity_name}/signup?email={email1}")
    test_client.post(f"/activities/{activity_name}/signup?email={email2}")
    response = test_client.get("/activities")
    participants = response.json()[activity_name]["participants"]
    
    # Assert
    assert email1 in participants
    assert email2 in participants
