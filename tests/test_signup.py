"""
Tests for the POST /activities/{activity_name}/signup endpoint.

Uses the AAA (Arrange-Act-Assert) testing pattern:
- Arrange: Set up test data and prerequisites
- Act: Execute the code being tested
- Assert: Verify the results
"""

import pytest


class TestSignupForActivity:
    """Tests for signing up a student for an activity."""
    
    def test_signup_successful_with_valid_activity_and_email(self, client):
        """
        Test successful signup for an activity with a new email.
        
        Arrange: Prepare a valid activity name and new email
        Act: Make a POST request to signup endpoint
        Assert: Verify the response status is 200 and success message is returned
        """
        # Arrange
        activity_name = "Chess Club"
        email = "newemail@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert "message" in response.json()
        assert email in response.json()["message"]
        assert activity_name in response.json()["message"]
    
    def test_signup_adds_email_to_participants(self, client):
        """
        Test that signup actually adds the email to the activity participants.
        
        Arrange: Prepare a valid activity name and new email
        Act: Sign up the email, then retrieve activities
        Assert: Verify the email appears in the activity's participants list
        """
        # Arrange
        activity_name = "Chess Club"
        email = "test@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        activities_response = client.get("/activities")
        activities = activities_response.json()
        
        # Assert
        assert response.status_code == 200
        assert email in activities[activity_name]["participants"]
    
    def test_signup_nonexistent_activity_returns_404(self, client):
        """
        Test that signup for a non-existent activity returns 404.
        
        Arrange: Prepare a non-existent activity name
        Act: Attempt to sign up for the non-existent activity
        Assert: Verify the response status is 404
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "test@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_signup_duplicate_email_returns_400(self, client):
        """
        Test that signup with an already registered email returns 400.
        
        Arrange: Choose an activity and an email already registered
        Act: Attempt to sign up the same email again
        Assert: Verify the response status is 400
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already registered in fixture
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"].lower()
    
    def test_signup_multiple_students_same_activity(self, client):
        """
        Test that multiple students can sign up for the same activity.
        
        Arrange: Prepare two different emails
        Act: Sign up both emails for the same activity
        Assert: Verify both emails are in the activity's participants
        """
        # Arrange
        activity_name = "Chess Club"
        email1 = "student1@mergington.edu"
        email2 = "student2@mergington.edu"
        
        # Act
        response1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email1}
        )
        response2 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email2}
        )
        activities_response = client.get("/activities")
        activities = activities_response.json()
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert email1 in activities[activity_name]["participants"]
        assert email2 in activities[activity_name]["participants"]
