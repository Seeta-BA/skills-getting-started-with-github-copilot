"""
Tests for the GET / (root) endpoint.

Uses the AAA (Arrange-Act-Assert) testing pattern:
- Arrange: Set up test data and prerequisites
- Act: Execute the code being tested
- Assert: Verify the results
"""

import pytest


class TestRootEndpoint:
    """Tests for the root endpoint."""
    
    def test_root_returns_redirect(self, client):
        """
        Test that GET / returns a redirect response.
        
        Arrange: No specific setup needed
        Act: Make a GET request to the root endpoint
        Assert: Verify the response is a redirect (status code 307)
        """
        # Arrange
        # (No setup needed)
        
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code in [301, 302, 303, 307, 308]
    
    def test_root_redirects_to_static_index(self, client):
        """
        Test that GET / redirects to /static/index.html.
        
        Arrange: No specific setup needed
        Act: Make a GET request to the root endpoint (with redirect following)
        Assert: Verify the response contains content from index.html
        """
        # Arrange
        # (No setup needed)
        
        # Act
        response = client.get("/", follow_redirects=True)
        
        # Assert
        assert response.status_code == 200
        # Check that response contains HTML content from static files
        assert "<!DOCTYPE html>" in response.text or "<html" in response.text
    
    def test_root_location_header_points_to_static(self, client):
        """
        Test that the Location header in redirect points to /static/index.html.
        
        Arrange: No specific setup needed
        Act: Make a GET request to the root endpoint without following redirects
        Assert: Verify the Location header contains /static/index.html
        """
        # Arrange
        # (No setup needed)
        
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert "location" in response.headers
        assert response.headers["location"] == "/static/index.html"
