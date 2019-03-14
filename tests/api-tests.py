import unittest
import json
import requests

URL = 'http://127.0.0.1:8080/{post_method}'


class ApiTests(unittest.TestCase):
    """Testing our api by sending different posts"""

    def test_add_company(self):
        url = URL.format(post_method='add_company')
        valid_data = json.dumps({'company': 'intel'}).encode('utf-8')
        code = requests.post(url, valid_data).status_code
        self.assertEqual(code, 200)
        bad_data = json.dumps({'bad_company': 'intel'}).encode('utf-8')
        code = requests.post(url, bad_data).status_code
        self.assertEqual(code, 400)

    def test_add_worker(self):
        url = URL.format(post_method='add_worker')
        valid_data = json.dumps({'name' : 'Dmitry', 'company': 'intel'}).encode('utf-8')
        code = requests.post(url, valid_data).status_code
        self.assertEqual(code, 200)
        bad_data = json.dumps({'name' : 'Dmitry', 'company' : 'not existing company'}).encode('utf-8')
        code = requests.post(url, bad_data).status_code
        self.assertEqual(code, 400)

