import unittest
import json
import requests

URL = 'http://127.0.0.1:8080/{post_method}'


class ApiTests(unittest.TestCase):
    """Testing our api by sending different posts"""

    def test_add_company(self):
        url = URL.format(post_method='add_company')
        valid_data = json.dumps(
            {'company': 'Avito'}).encode('utf-8')
        code = requests.post(url, valid_data).status_code
        self.assertEqual(code, 200)
        bad_data = json.dumps({'bad_company': 'intel'}).encode('utf-8')
        code = requests.post(url, bad_data).status_code
        self.assertEqual(code, 400)
        not_json = {'company': 'amd'}
        code = requests.post(url, not_json).status_code
        self.assertEqual(code, 400)
        not_str = json.dumps(
            {'company': 123}).encode('utf-8')
        self.assertEqual(code, 400)

    def test_add_worker(self):
        url = URL.format(post_method='add_worker')
        valid_data = json.dumps(
            {'name': 'Dmitry', 'company': 'Avito'}).encode('utf-8')
        code = requests.post(url, valid_data).status_code
        self.assertEqual(code, 200)
        bad_data = json.dumps(
            {'name': 'Dmitry', 'company': 'not existing company'}).encode('utf-8')
        code = requests.post(url, bad_data).status_code
        self.assertEqual(code, 400)
        not_str = json.dumps(
            {'name': 123}).encode('utf-8')
        self.assertEqual(code, 400)

    def test_add_products(self):
        url = URL.format(post_method='add_product')
        valid_data = json.dumps(
            {'name': 'Car'}).encode('utf-8')
        code = requests.post(url, valid_data).status_code
        self.assertEqual(code, 200)
        bad_data = json.dumps(
            {'bad_name': 'not product'}).encode('utf-8')
        code = requests.post(url, bad_data).status_code
        self.assertEqual(code, 400)
        not_str = json.dumps(
            {'name': 123}).encode('utf-8')
        self.assertEqual(code, 400)

    def test_add_edit_responsible(self):
        url = URL.format(post_method='edit_responsible')
        valid_data = json.dumps(
            {'worker_id': 1, 'product_id': 1}).encode('utf-8')
        code = requests.post(url, valid_data).status_code
        self.assertEqual(code, 200)
        bad_data = json.dumps(
            {'worker_id': 999, 'product_id': 1}).encode('utf-8')
        code = requests.post(url, bad_data).status_code
        self.assertEqual(code, 400)
        bad_data = json.dumps(
            {'worker_id': 'string', 'product_id': 1}).encode('utf-8')
        code = requests.post(url, bad_data).status_code
        self.assertEqual(code, 400)
