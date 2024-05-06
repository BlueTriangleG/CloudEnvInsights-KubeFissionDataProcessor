import unittest, requests, json, time

class HTTPSession:
    def __init__(self, protocol, hostname, port):
        self.session = requests.session()
        self.base_url = f'{protocol}://{hostname}:{port}'

    def get(self, path):
        return self.session.get(f'{self.base_url}{path}')

    def post(self, path, data):
        return self.session.post(f'{self.base_url}{path}', json=data)

    def put(self, path, data):
        return self.session.put(f'{self.base_url}{path}', json=data)

    def delete(self, path):
        return self.session.delete(f'{self.base_url}{path}')

class TestEnd2End(unittest.TestCase):

    def setUp(self):
        self.assertEqual(test_request.delete('/wipedatabase').status_code, 200)
        time.sleep(1)

    def test_student(self):
        self.assertEqual(test_request.put('/students/1', {'name': 'John Doe', 'courses': '90024'}).status_code, 201)
        self.assertEqual(test_request.put('/students/2', {'name': 'Jane Doe', 'courses': ['90024', '90059']}).status_code, 201)
        time.sleep(1)

        r= test_request.get('/students/1')
        self.assertEqual(r.status_code, 200)
        o= r.json()['_source']
        self.assertEqual(o['name'], 'John Doe')
        self.assertEqual(o['courses'], '90024')

        r= test_request.get('/students/2')
        o= r.json()['_source']
        self.assertEqual(r.status_code, 200)
        self.assertEqual(o['name'], 'Jane Doe')
        self.assertEqual(o['courses'], ['90024', '90059'])

        r= test_request.put('/students/1', {'name': 'Bob Carr', 'courses': '90024'})
        self.assertEqual(r.status_code, 200)
        r= test_request.get('/students/1')
        o= r.json()['_source']
        self.assertEqual(r.status_code, 200)
        self.assertEqual(o['name'], 'Bob Carr')
        self.assertEqual(o['courses'], '90024')

        self.assertEqual(test_request.get('/students/999').status_code, 404)

        self.assertEqual(test_request.delete('/students/1').status_code, 200)
        self.assertEqual(test_request.delete('/students/2').status_code, 200)

    def test_students(self):
        self.assertEqual(test_request.put('/courses/90024', {'name': 'Cloud Computing'}).status_code, 201)
        self.assertEqual(test_request.put('/courses/90059', {'name': 'Introduction to Programming'}).status_code, 201)
        self.assertEqual(test_request.put('/students/1', {'name': 'John Doe', 'courses': '90024'}).status_code, 201)
        self.assertEqual(test_request.put('/students/2', {'name': 'Jane Doe', 'courses': ['90024', '90059']}).status_code, 201)
        time.sleep(1)

        r= test_request.get('/students')
        o= (r.json()['hits'])['hits']
        self.assertEqual(r.status_code, 200)
        self.assertEqual(o[0]['fields']['name'][0], 'Jane Doe')
        self.assertEqual(o[1]['fields']['name'][0], 'John Doe')

    def test_course(self):
        self.assertEqual(test_request.put('/courses/90024', {'name': 'Cloud x Computing'}).status_code, 201)
        self.assertEqual(test_request.put('/courses/90059', {'name': 'Introduction to Programming'}).status_code, 201)
        time.sleep(1)

        r= test_request.get('/courses/90024')
        o= r.json()['_source']
        self.assertEqual(r.status_code, 200)
        self.assertEqual(o['name'], 'Cloud x Computing')

        r= test_request.get('/courses/90059')
        o= r.json()['_source']
        self.assertEqual(r.status_code, 200)
        self.assertEqual(o['name'], 'Introduction to Programming')

        r= test_request.put('/courses/90024', {'name': 'Cloud Computing'})
        self.assertEqual(r.status_code, 200)
        r= test_request.get('/courses/90024')
        o= r.json()['_source']
        self.assertEqual(r.status_code, 200)
        self.assertEqual(o['name'], 'Cloud Computing')

        self.assertEqual(test_request.get('/courses/999').status_code, 404)

        self.assertEqual(test_request.delete('/courses/90024').status_code, 200)
        self.assertEqual(test_request.delete('/courses/90059').status_code, 200)

    def test_courses(self):
        self.assertEqual(test_request.put('/courses/90024', {'name': 'Cloud Computing'}).status_code, 201)
        self.assertEqual(test_request.put('/courses/90059', {'name': 'Introduction to Programming'}).status_code, 201)
        time.sleep(1)

        r= test_request.get('/courses')
        o= (r.json()['hits'])['hits']
        self.assertEqual(r.status_code, 200)
        self.assertEqual(o[0]['fields']['name'][0], 'Cloud Computing')
        self.assertEqual(o[1]['fields']['name'][0], 'Introduction to Programming')

    def test_courses_students(self):
        self.assertEqual(test_request.put('/courses/90024', {'name': 'Cloud Computing'}).status_code, 201)
        self.assertEqual(test_request.put('/courses/90059', {'name': 'Introduction to Programming'}).status_code, 201)
        self.assertEqual(test_request.put('/students/1', {'name': 'John Doe', 'courses': '90024'}).status_code, 201)
        self.assertEqual(test_request.put('/students/2', {'name': 'Jane Doe', 'courses': ['90024', '90059']}).status_code, 201)
        time.sleep(1)

        r= test_request.get('/courses/90024/students')
        o= (r.json()['hits'])['hits']
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(o), 2)
        self.assertEqual(o[0]['fields']['name'][0], 'Jane Doe')
        self.assertEqual(o[1]['fields']['name'][0], 'John Doe')

        r= test_request.get('/courses/90059/students')
        o= (r.json()['hits'])['hits']
        self.assertEqual(len(o), 1)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(o[0]['fields']['name'][0], 'Jane Doe')

        r= test_request.get('/courses/99999/students')
        o= (r.json()['hits'])['hits']
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(o), 0)

if __name__ == '__main__':

    test_request = HTTPSession('http', 'localhost', 9090)
    unittest.main()
