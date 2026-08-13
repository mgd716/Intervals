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

from update_map import fetch_gps_stream

def test_fetch_gps_stream_happy_path():
    """
    Test that fetch_gps_stream successfully parses valid latlng data and correctly downsamples (every 4th element).
    """
    with patch("update_map.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        # 8 elements to test downsampling [::4] -> should return elements at index 0 and 4
        mock_response.json.return_value = [
            {
                "type": "latlng",
                "data": [10.123456, 11.1, 12.1, 13.1, 14.987654, 15.1, 16.1, 17.1],
                "data2": [20.123456, 21.1, 22.1, 23.1, 24.987654, 25.1, 26.1, 27.1]
            }
        ]
        mock_get.return_value = mock_response

        result = fetch_gps_stream("123")
        # Expect downsampling: index 0 and index 4, rounded to 5 decimal places
        assert result == [[10.12346, 20.12346], [14.98765, 24.98765]]

def test_fetch_gps_stream_missing_keys():
    """
    Test fetch_gps_stream when the stream dictionary is missing expected keys like 'type' or 'data'.
    """
    with patch("update_map.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"data": [10.0], "data2": [20.0]}, # Missing 'type'
            {"type": "latlng", "data2": [20.0]}, # Missing 'data'
            {"type": "latlng", "data": [10.0]} # Missing 'data2'
        ]
        mock_get.return_value = mock_response

        result = fetch_gps_stream("123")
        assert result is None

def test_fetch_gps_stream_empty_lists():
    """
    Test fetch_gps_stream when data or data2 are empty lists.
    """
    with patch("update_map.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                "type": "latlng",
                "data": [],
                "data2": []
            }
        ]
        mock_get.return_value = mock_response

        result = fetch_gps_stream("123")
        assert result is None

def test_fetch_gps_stream_none_values():
    """
    Test fetch_gps_stream when data or data2 contain None values.
    """
    with patch("update_map.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                "type": "latlng",
                "data": [10.1, None, 10.3, 10.4, 10.5],
                "data2": [20.1, 20.2, None, 20.4, 20.5]
            }
        ]
        mock_get.return_value = mock_response

        result = fetch_gps_stream("123")
        # index 0 is valid. index 1 and 2 contain None and are skipped. index 3 is [10.4, 20.4], index 4 is [10.5, 20.5]
        # zip produces:
        # (10.1, 20.1) -> valid
        # (None, 20.2) -> skipped
        # (10.3, None) -> skipped
        # (10.4, 20.4) -> valid
        # (10.5, 20.5) -> valid
        # Filtered list: [[10.1, 20.1], [10.4, 20.4], [10.5, 20.5]]
        # Downsampled [::4]: only the 0th element should be returned
        assert result == [[10.1, 20.1]]

def test_fetch_gps_stream_not_a_list():
    """
    Test fetch_gps_stream when the JSON response is not a list.
    """
    with patch("update_map.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"type": "latlng", "data": [10.0], "data2": [20.0]} # Dict instead of list
        mock_get.return_value = mock_response

        result = fetch_gps_stream("123")
        assert result is None

@pytest.mark.parametrize("lat, lon, zoom, expected", [
    # Null Island
    (0.0, 0.0, 0, "0_0_0"),
    (0.0, 0.0, 14, "14_8192_8192"),
    # San Francisco approx
    (37.7749, -122.4194, 14, "14_2620_6332"),
    # London approx
    (51.5074, -0.1278, 14, "14_8186_5448"),
    # Sydney approx
    (-33.8688, 151.2093, 14, "14_15073_9831"),
    # Edge cases - Web Mercator max/min limits
    # Max latitude is approximately 85.0511
    (85.0511, 180.0, 14, "14_16384_0"),
    (-85.0511, -180.0, 14, "14_0_16383"),
])
def test_get_tile(lat, lon, zoom, expected):
    from update_map import get_tile
    assert get_tile(lat, lon, zoom) == expected
