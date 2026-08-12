import pytest
from unittest.mock import patch, MagicMock
from update_map import fetch_wellness_data, fetch_activities

def test_fetch_wellness_data_error_handling(capsys):
    """
    Test that fetch_wellness_data returns an empty list and prints an error message
    when the API request returns a non-200 status code.
    """
    with patch("update_map.requests.get") as mock_get:
        # Create a mock response object
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        # Call the function
        result = fetch_wellness_data()

        # Assert the result is an empty list
        assert result == []

        # Assert the correct error message was printed
        captured = capsys.readouterr()
        assert "Failed to fetch wellness data: 500" in captured.out

def test_fetch_activities_error_handling():
    """
    Test that fetch_activities raises an Exception when the API request returns a non-200 status code.
    """
    with patch("update_map.requests.get") as mock_get:
        # Create a mock response object
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        # Verify that the expected exception is raised
        with pytest.raises(Exception, match="Failed to fetch activities list: 500"):
            fetch_activities()
