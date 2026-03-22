import pytest


def test_unregister_success(test_client, reset_activities):
    """Test successful unregister from an activity"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already registered in fixture
    
    # Act
    response = test_client.post(
        f"/activities/{activity_name}/unregister?email={email}"
    )
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    assert "Unregistered" in data["message"]
    assert email in data["message"]


def test_unregister_removes_participant(test_client, reset_activities):
    """Test that unregister actually removes participant from list"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    
    # Act
    test_client.post(f"/activities/{activity_name}/unregister?email={email}")
    response = test_client.get("/activities")
    participants = response.json()[activity_name]["participants"]
    
    # Assert
    assert email not in participants


def test_unregister_nonexistent_activity(test_client, reset_activities):
    """Test unregister from non-existent activity"""
    # Arrange
    nonexistent_activity = "Fake Activity"
    email = "student@mergington.edu"
    
    # Act
    response = test_client.post(
        f"/activities/{nonexistent_activity}/unregister?email={email}"
    )
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_not_registered(test_client, reset_activities):
    """Test unregister when student is not registered"""
    # Arrange
    activity_name = "Chess Club"
    email = "notregistered@mergington.edu"
    
    # Act
    response = test_client.post(
        f"/activities/{activity_name}/unregister?email={email}"
    )
    
    # Assert
    assert response.status_code == 400
    assert "not registered for this activity" in response.json()["detail"]


def test_unregister_then_respaces_for_others(test_client, reset_activities):
    """Test that unregistering frees up a spot for new signup"""
    # Arrange
    activities_data = test_client.get("/activities").json()
    
    # Find a full activity
    full_activity_name = None
    full_activity_participant = None
    for activity_name, activity_data in activities_data.items():
        if len(activity_data["participants"]) >= activity_data["max_participants"]:
            full_activity_name = activity_name
            full_activity_participant = activity_data["participants"][0]
            break
    
    new_student_email = "newstudent@mergington.edu"
    
    # Act - Unregister to free up a spot
    test_client.post(
        f"/activities/{full_activity_name}/unregister?email={full_activity_participant}"
    )
    
    # Act - New student signs up to the freed spot
    response = test_client.post(
        f"/activities/{full_activity_name}/signup?email={new_student_email}"
    )
    
    # Assert
    assert response.status_code == 200
