"""Test cases for the High School Management System API - Single Responsibility Tests"""

import pytest
from fastapi.testclient import TestClient
from src.app import activities


class TestRootEndpoint:
    """Tests for the root endpoint"""

    def test_root_returns_redirect_status(self, client):
        """Test that root endpoint returns a redirect status code"""
        # Arrange & Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307

    def test_root_redirects_to_static_index(self, client):
        """Test that root endpoint redirects to the correct static file"""
        # Arrange & Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert "/static/index.html" in response.headers["location"]


class TestGetActivities:
    """Tests for the GET /activities endpoint"""

    def test_get_activities_returns_success_status(self, client, reset_activities):
        """Test that GET /activities returns a successful response"""
        # Arrange & Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200

    def test_get_activities_returns_dictionary(self, client, reset_activities):
        """Test that GET /activities returns a dictionary"""
        # Arrange & Act
        response = client.get("/activities")

        # Assert
        data = response.json()
        assert isinstance(data, dict)

    def test_get_activities_includes_chess_club(self, client, reset_activities):
        """Test that GET /activities includes Chess Club"""
        # Arrange & Act
        response = client.get("/activities")

        # Assert
        data = response.json()
        assert "Chess Club" in data

    def test_get_activities_includes_programming_class(self, client, reset_activities):
        """Test that GET /activities includes Programming Class"""
        # Arrange & Act
        response = client.get("/activities")

        # Assert
        data = response.json()
        assert "Programming Class" in data

    def test_get_activities_includes_basketball_team(self, client, reset_activities):
        """Test that GET /activities includes Basketball Team"""
        # Arrange & Act
        response = client.get("/activities")

        # Assert
        data = response.json()
        assert "Basketball Team" in data

    def test_chess_club_has_description_field(self, client, reset_activities):
        """Test that Chess Club activity has description field"""
        # Arrange & Act
        response = client.get("/activities")

        # Assert
        data = response.json()
        assert "description" in data["Chess Club"]

    def test_chess_club_has_schedule_field(self, client, reset_activities):
        """Test that Chess Club activity has schedule field"""
        # Arrange & Act
        response = client.get("/activities")

        # Assert
        data = response.json()
        assert "schedule" in data["Chess Club"]

    def test_chess_club_has_max_participants_field(self, client, reset_activities):
        """Test that Chess Club activity has max_participants field"""
        # Arrange & Act
        response = client.get("/activities")

        # Assert
        data = response.json()
        assert "max_participants" in data["Chess Club"]

    def test_chess_club_has_participants_field(self, client, reset_activities):
        """Test that Chess Club activity has participants field"""
        # Arrange & Act
        response = client.get("/activities")

        # Assert
        data = response.json()
        assert "participants" in data["Chess Club"]

    def test_chess_club_participants_is_list(self, client, reset_activities):
        """Test that Chess Club participants field is a list"""
        # Arrange & Act
        response = client.get("/activities")

        # Assert
        data = response.json()
        assert isinstance(data["Chess Club"]["participants"], list)

    def test_get_activities_returns_nine_activities(self, client, reset_activities):
        """Test that GET /activities returns exactly nine activities"""
        # Arrange & Act
        response = client.get("/activities")

        # Assert
        data = response.json()
        assert len(data) == 9


class TestSignupEndpoint:
    """Tests for the POST /activities/{activity_name}/signup endpoint"""

    def test_signup_returns_success_status_for_valid_request(self, client, reset_activities):
        """Test that signup returns success status for valid request"""
        # Arrange
        email = "newstudent@mergington.edu"
        activity = "Chess Club"

        # Act
        response = client.post(f"/activities/{activity}/signup?email={email}")

        # Assert
        assert response.status_code == 200

    def test_signup_returns_message_in_response(self, client, reset_activities):
        """Test that signup response contains a message field"""
        # Arrange
        email = "newstudent@mergington.edu"
        activity = "Chess Club"

        # Act
        response = client.post(f"/activities/{activity}/signup?email={email}")

        # Assert
        data = response.json()
        assert "message" in data

    def test_signup_message_contains_signed_up_text(self, client, reset_activities):
        """Test that signup message contains 'Signed up' text"""
        # Arrange
        email = "newstudent@mergington.edu"
        activity = "Chess Club"

        # Act
        response = client.post(f"/activities/{activity}/signup?email={email}")

        # Assert
        data = response.json()
        assert "Signed up" in data["message"]

    def test_signup_message_contains_email(self, client, reset_activities):
        """Test that signup message contains the email address"""
        # Arrange
        email = "newstudent@mergington.edu"
        activity = "Chess Club"

        # Act
        response = client.post(f"/activities/{activity}/signup?email={email}")

        # Assert
        data = response.json()
        assert email in data["message"]

    def test_signup_adds_email_to_participants_list(self, client, reset_activities):
        """Test that signup adds the email to the activity's participants list"""
        # Arrange
        email = "newstudent@mergington.edu"
        activity = "Chess Club"

        # Act
        client.post(f"/activities/{activity}/signup?email={email}")

        # Assert
        response = client.get("/activities")
        activities_data = response.json()
        assert email in activities_data[activity]["participants"]

    def test_signup_returns_404_for_nonexistent_activity(self, client, reset_activities):
        """Test that signup returns 404 for non-existent activity"""
        # Arrange
        email = "test@mergington.edu"
        nonexistent_activity = "Nonexistent Activity"

        # Act
        response = client.post(f"/activities/{nonexistent_activity}/signup?email={email}")

        # Assert
        assert response.status_code == 404

    def test_signup_error_contains_detail_for_nonexistent_activity(self, client, reset_activities):
        """Test that signup error response contains detail for non-existent activity"""
        # Arrange
        email = "test@mergington.edu"
        nonexistent_activity = "Nonexistent Activity"

        # Act
        response = client.post(f"/activities/{nonexistent_activity}/signup?email={email}")

        # Assert
        data = response.json()
        assert "detail" in data

    def test_signup_error_detail_contains_activity_not_found(self, client, reset_activities):
        """Test that signup error detail contains 'Activity not found'"""
        # Arrange
        email = "test@mergington.edu"
        nonexistent_activity = "Nonexistent Activity"

        # Act
        response = client.post(f"/activities/{nonexistent_activity}/signup?email={email}")

        # Assert
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_signup_returns_400_for_already_registered_student(self, client, reset_activities):
        """Test that signup returns 400 when student is already registered"""
        # Arrange
        email = "michael@mergington.edu"  # Already in Chess Club
        activity = "Chess Club"

        # Act
        response = client.post(f"/activities/{activity}/signup?email={email}")

        # Assert
        assert response.status_code == 400

    def test_signup_error_detail_contains_already_signed_up(self, client, reset_activities):
        """Test that signup error detail contains 'already signed up'"""
        # Arrange
        email = "michael@mergington.edu"  # Already in Chess Club
        activity = "Chess Club"

        # Act
        response = client.post(f"/activities/{activity}/signup?email={email}")

        # Assert
        data = response.json()
        assert "already signed up" in data["detail"]

    def test_signup_increases_participant_count_by_one(self, client, reset_activities):
        """Test that signup increases the participant count by exactly one"""
        # Arrange
        email = "newstudent@mergington.edu"
        activity = "Chess Club"
        original_count = len(activities[activity]["participants"])

        # Act
        client.post(f"/activities/{activity}/signup?email={email}")

        # Assert
        response = client.get("/activities")
        data = response.json()
        assert len(data[activity]["participants"]) == original_count + 1


class TestUnregisterEndpoint:
    """Tests for the DELETE /activities/{activity_name}/unregister endpoint"""

    def test_unregister_returns_success_status_for_valid_request(self, client, reset_activities):
        """Test that unregister returns success status for valid request"""
        # Arrange
        email = "michael@mergington.edu"
        activity = "Chess Club"

        # Act
        response = client.delete(f"/activities/{activity}/unregister?email={email}")

        # Assert
        assert response.status_code == 200

    def test_unregister_returns_message_in_response(self, client, reset_activities):
        """Test that unregister response contains a message field"""
        # Arrange
        email = "michael@mergington.edu"
        activity = "Chess Club"

        # Act
        response = client.delete(f"/activities/{activity}/unregister?email={email}")

        # Assert
        data = response.json()
        assert "message" in data

    def test_unregister_message_contains_removed_text(self, client, reset_activities):
        """Test that unregister message contains 'Removed' text"""
        # Arrange
        email = "michael@mergington.edu"
        activity = "Chess Club"

        # Act
        response = client.delete(f"/activities/{activity}/unregister?email={email}")

        # Assert
        data = response.json()
        assert "Removed" in data["message"]

    def test_unregister_message_contains_email(self, client, reset_activities):
        """Test that unregister message contains the email address"""
        # Arrange
        email = "michael@mergington.edu"
        activity = "Chess Club"

        # Act
        response = client.delete(f"/activities/{activity}/unregister?email={email}")

        # Assert
        data = response.json()
        assert email in data["message"]

    def test_unregister_removes_email_from_participants_list(self, client, reset_activities):
        """Test that unregister removes the email from the activity's participants list"""
        # Arrange
        email = "michael@mergington.edu"
        activity = "Chess Club"

        # Act
        client.delete(f"/activities/{activity}/unregister?email={email}")

        # Assert
        response = client.get("/activities")
        activities_data = response.json()
        assert email not in activities_data[activity]["participants"]

    def test_unregister_returns_404_for_nonexistent_activity(self, client, reset_activities):
        """Test that unregister returns 404 for non-existent activity"""
        # Arrange
        email = "test@mergington.edu"
        nonexistent_activity = "Nonexistent Activity"

        # Act
        response = client.delete(f"/activities/{nonexistent_activity}/unregister?email={email}")

        # Assert
        assert response.status_code == 404

    def test_unregister_error_detail_contains_activity_not_found(self, client, reset_activities):
        """Test that unregister error detail contains 'Activity not found'"""
        # Arrange
        email = "test@mergington.edu"
        nonexistent_activity = "Nonexistent Activity"

        # Act
        response = client.delete(f"/activities/{nonexistent_activity}/unregister?email={email}")

        # Assert
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_unregister_returns_404_for_not_signed_up_student(self, client, reset_activities):
        """Test that unregister returns 404 when student is not signed up"""
        # Arrange
        email = "notsignedup@mergington.edu"
        activity = "Chess Club"

        # Act
        response = client.delete(f"/activities/{activity}/unregister?email={email}")

        # Assert
        assert response.status_code == 404

    def test_unregister_error_detail_contains_not_signed_up(self, client, reset_activities):
        """Test that unregister error detail contains 'not signed up'"""
        # Arrange
        email = "notsignedup@mergington.edu"
        activity = "Chess Club"

        # Act
        response = client.delete(f"/activities/{activity}/unregister?email={email}")

        # Assert
        data = response.json()
        assert "not signed up" in data["detail"]

    def test_unregister_decreases_participant_count_by_one(self, client, reset_activities):
        """Test that unregister decreases the participant count by exactly one"""
        # Arrange
        email_to_remove = "emma@mergington.edu"
        activity = "Programming Class"
        original_count = len(activities[activity]["participants"])

        # Act
        client.delete(f"/activities/{activity}/unregister?email={email_to_remove}")

        # Assert
        response = client.get("/activities")
        data = response.json()
        assert len(data[activity]["participants"]) == original_count - 1


class TestSignupUnregisterIntegration:
    """Integration tests for signup and unregister workflows"""

    def test_signup_then_unregister_returns_success_for_signup(self, client, reset_activities):
        """Test that signup works in a signup-then-unregister workflow"""
        # Arrange
        email = "workflow@mergington.edu"
        activity = "Chess Club"

        # Act
        response = client.post(f"/activities/{activity}/signup?email={email}")

        # Assert
        assert response.status_code == 200

    def test_signup_then_unregister_shows_participant_after_signup(self, client, reset_activities):
        """Test that participant appears in activity after signup"""
        # Arrange
        email = "workflow@mergington.edu"
        activity = "Chess Club"
        client.post(f"/activities/{activity}/signup?email={email}")

        # Act
        response = client.get("/activities")

        # Assert
        assert email in response.json()[activity]["participants"]

    def test_signup_then_unregister_returns_success_for_unregister(self, client, reset_activities):
        """Test that unregister works in a signup-then-unregister workflow"""
        # Arrange
        email = "workflow@mergington.edu"
        activity = "Chess Club"
        client.post(f"/activities/{activity}/signup?email={email}")

        # Act
        response = client.delete(f"/activities/{activity}/unregister?email={email}")

        # Assert
        assert response.status_code == 200

    def test_signup_then_unregister_removes_participant_after_unregister(self, client, reset_activities):
        """Test that participant is removed from activity after unregister"""
        # Arrange
        email = "workflow@mergington.edu"
        activity = "Chess Club"
        client.post(f"/activities/{activity}/signup?email={email}")
        client.delete(f"/activities/{activity}/unregister?email={email}")

        # Act
        response = client.get("/activities")

        # Assert
        assert email not in response.json()[activity]["participants"]