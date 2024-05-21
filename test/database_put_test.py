import unittest
import json
from unittest.mock import patch, mock_open
import requests
from requests.models import Response

# define the function sending data to cloud
def send_data_to_cloud(index_name, json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    BASE_URL = "http://127.0.0.1:9090/database"
    url = f"{BASE_URL}/{index_name}"
    
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, json=data)
    
    return response


class TestSendDataToCloud(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data='[{"BMP2_5": 7.740714285714288, "datetime_local": "2024-05-18-19", "location_name": "Melbourne"}]')
    @patch('requests.post')
    def test_send_data_to_cloud_success(self, mock_post, mock_file):
        # Mock the response to simulate a successful HTTP request
        mock_response = Response()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        response = send_data_to_cloud('aircondition', 'dummy_path')
        self.assertEqual(response.status_code, 200)
        mock_post.assert_called_once_with(
            'http://127.0.0.1:9090/database/aircondition',
            headers={'Content-Type': 'application/json'},
            json=[{"BMP2_5": 7.740714285714288, "datetime_local": "2024-05-18-19", "location_name": "Melbourne"}]
        )

    @patch('builtins.open', new_callable=mock_open, read_data='[{"BMP2_5": 7.740714285714288, "datetime_local": "2024-05-18-19", "location_name": "Melbourne"}]')
    @patch('requests.post')
    def test_send_data_to_cloud_failure(self, mock_post, mock_file):
        # Mock the response to simulate a failed HTTP request
        mock_response = Response()
        mock_response.status_code = 500
        mock_response._content = b'Internal Server Error'
        mock_post.return_value = mock_response

        response = send_data_to_cloud('aircondition', 'dummy_path')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.text, 'Internal Server Error')

if __name__ == '__main__':
    unittest.main()
