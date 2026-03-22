import pytest


def test_get_activities(test_client, reset_activities):
    """Test retrieving all activities"""
    # Arrange
    # No setup needed - using fixtures
    
    # Act
    response = test_client.get("/activities")
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_activities_structure(test_client, reset_activities):
    """Test that activities have correct structure"""
    # Arrange
    # No setup needed - using fixtures
    
    # Act
    response = test_client.get("/activities")
    data = response.json()
    activity = data["Chess Club"]
    
    # Assert
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity
    assert isinstance(activity["participants"], list)


def test_activities_participants_count(test_client, reset_activities):
    """Test that participant counts are correct"""
    # Arrange
    expected_chess_club_count = 4
    expected_participant = "michael@mergington.edu"
    
    # Act
    response = test_client.get("/activities")
    data = response.json()
    chess_club_participants = data["Chess Club"]["participants"]
    
    # Assert
    assert len(chess_club_participants) == expected_chess_club_count
    assert expected_participant in chess_club_participants
