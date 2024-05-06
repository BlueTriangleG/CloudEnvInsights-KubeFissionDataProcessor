import unittest, json, time, sys
from unittest.mock import MagicMock
sys.path.append('./functions/library')
from Commons import Commons
from ESCourse import ESCourse
from ESStudent import ESStudent
from flask import request, current_app

class TestUnit(unittest.TestCase):

    def setUp(self):
        self.mock_commons = MagicMock(autospec=Commons)
        self.mock_commons.config = MagicMock(return_value='x')
        self.mock_request = MagicMock(autospec=request)
        self.mock_request.headers ={'X-Fission-Params-Courseid': 'comp90024'}
        self.mock_request.headers ={'X-Fission-Params-Studentid': '123'}

    def test_escourse(self):
        test_escourse= ESCourse(self.mock_commons, self.mock_request)
        self.assertEqual(test_escourse.url(), 'x/x/_doc/course_comp90024')

    def test_escourse(self):
        test_esstudent= ESStudent(self.mock_commons, self.mock_request)
        self.assertEqual(test_esstudent.url(), 'x/x/_doc/student_123')

if __name__ == '__main__':
    unittest.main()
