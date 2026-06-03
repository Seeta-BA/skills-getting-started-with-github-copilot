"""
Tests for the GET /activities endpoint.

Uses the AAA (Arrange-Act-Assert) testing pattern:
- Arrange: Set up test data and prerequisites
- Act: Execute the code being tested
- Assert: Verify the results
"""

import pytest


class TestGetActivities:
    """Tests for retrieving all activities."""
    
    def test_get_activities_returns_success(self, client):
        """
        Test that GET /activities returns a 200 status code.
        
        Arrange: No specific setup needed (uses default fixture data)
        Act: Make a GET request to /activities
        Assert: Verify the response status code is 200
        """
        # Arrange
        # (No setup needed - using fixture data)
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
    
    def test_get_activities_returns_all_activities(self, client):
        """
        Test that GET /activities returns all activities.
        
        Arrange: No specific setup needed (uses default fixture data)
        Act: Make a GET request to /activities
        Assert: Verify the response contains all 9 activities
        """
        # Arrange
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Soccer Team",
            "Basketball Club",
            "Art Studio",
            "Drama Club",
            "Math Olympiad",
            "Robotics Workshop"
        ]
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert len(data) == 9
        for activity_name in expected_activities:
            assert activity_name in data
    
    def test_get_activities_contains_required_fields(self, client):
        """
        Test that each activity has all required fields.
        
        Arrange: No specific setup needed (uses default fixture data)
        Act: Make a GET request to /activities
        Assert: Verify each activity contains description, schedule, 
                max_participants, and participants fields
        """
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data, dict)
            assert required_fields.issubset(activity_data.keys())
    
    def test_get_activities_participants_is_list(self, client):
        """
        Test that participants field is a list for each activity.
        
        Arrange: No specific setup needed (uses default fixture data)
        Act: Make a GET request to /activities
        Assert: Verify the participants field is a list
        """
        # Arrange
        # (No setup needed - using fixture data)
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["participants"], list)
