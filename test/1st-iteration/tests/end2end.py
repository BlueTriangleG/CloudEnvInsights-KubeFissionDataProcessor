import unittest
import requests
import json
from unittest.mock import patch

class HTTPSession:
    def __init__(self, protocol, hostname, port):
        self.session = requests.Session()
        self.base_url = f'{protocol}://{hostname}:{port}'

    def get(self, path):
        return self.session.get(f'{self.base_url}/{path}')

    def post(self, path, data):
        return self.session.post(f'{self.base_url}/{path}', data)

    def put(self, path, data):
        return self.session.put(f'{self.base_url}/{path}', data)

    def delete(self, path):
        return self.session.delete(f'{self.base_url}/{path}')

class TestEnd2End(unittest.TestCase):
    def test_student(self):
        self.assertEqual(test_request.get('/students/111').status_code, 200)
        self.assertEqual(test_request.get('/students/111').text, 'student')

        self.assertEqual(test_request.put('/students/111', {}).status_code, 200)
        self.assertEqual(test_request.put('/students/111', {}).text, 'student')

        self.assertEqual(test_request.delete('/students/111').status_code, 200)
        self.assertEqual(test_request.delete('/students/111').text, 'student')

    def test_students(self):
        self.assertEqual(test_request.get('/students').status_code, 200)
        self.assertEqual(test_request.get('/students').text, 'students')

    def test_course(self):
        self.assertEqual(test_request.get('/courses/111').status_code, 200)
        self.assertEqual(test_request.get('/courses/111').text, 'course')

        self.assertEqual(test_request.put('/courses/111', {}).status_code, 200)
        self.assertEqual(test_request.put('/courses/111', {}).text, 'course')

        self.assertEqual(test_request.delete('/courses/111').status_code, 200)
        self.assertEqual(test_request.delete('/courses/111').text, 'course')

    def test_courses(self):
        self.assertEqual(test_request.get('/courses').status_code, 200)
        self.assertEqual(test_request.get('/courses').text, 'courses')

        self.assertEqual(test_request.get('/courses/111/students').status_code, 200)
        self.assertEqual(test_request.get('/courses/111/students').text, 'coursesstudents')

if __name__ == '__main__':

    test_request = HTTPSession('http', 'localhost', 9090)
    unittest.main()
