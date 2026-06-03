"""
Tests for the DELETE /activities/{activity_name}/unregister endpoint.

Uses the AAA (Arrange-Act-Assert) testing pattern:
- Arrange: Set up test data and prerequisites
- Act: Execute the code being tested
- Assert: Verify the results
"""

import pytest


class TestUnregisterFromActivity:
    """Tests for unregistering a student from an activity."""
    
    def test_unregister_successful_for_registered_student(self, client):
        """
        Test successful unregistration of a student already in an activity.
        
        Arrange: Choose an activity and email that is registered
        Act: Make a DELETE request to unregister the student
        Assert: Verify the response status is 200 and success message is returned
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already registered in fixture
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert "message" in response.json()
        assert email in response.json()["message"]
        assert activity_name in response.json()["message"]
    
    def test_unregister_removes_email_from_participants(self, client):
        """
        Test that unregister actually removes the email from activity participants.
        
        Arrange: Choose an activity and email that is registered
        Act: Unregister the email, then retrieve activities
        Assert: Verify the email no longer appears in the activity's participants
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        activities_response = client.get("/activities")
        activities = activities_response.json()
        
        # Assert
        assert response.status_code == 200
        assert email not in activities[activity_name]["participants"]
    
    def test_unregister_nonexistent_activity_returns_404(self, client):
        """
        Test that unregister from a non-existent activity returns 404.
        
        Arrange: Prepare a non-existent activity name
        Act: Attempt to unregister from the non-existent activity
        Assert: Verify the response status is 404
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "test@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_unregister_nonregistered_student_returns_400(self, client):
        """
        Test that unregister of a non-registered student returns 400.
        
        Arrange: Choose a student email not registered for the activity
        Act: Attempt to unregister the student
        Assert: Verify the response status is 400
        """
        # Arrange
        activity_name = "Chess Club"
        email = "notregistered@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "not registered" in response.json()["detail"].lower()
    
    def test_unregister_then_signup_again(self, client):
        """
        Test that a student can unregister and then sign up again.
        
        Arrange: Choose an activity and email that is registered
        Act: Unregister the student, then sign them up again
        Assert: Verify both operations succeed and email is in participants
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act
        unregister_response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        activities_response = client.get("/activities")
        activities = activities_response.json()
        
        # Assert
        assert unregister_response.status_code == 200
        assert signup_response.status_code == 200
        assert email in activities[activity_name]["participants"]
