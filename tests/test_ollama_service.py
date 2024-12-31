import unittest
from unittest.mock import patch
from app import create_app

class TestOllamaService(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_ping_endpoint(self):
        response = self.client.get('/ping')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "ok"})

    def test_api_test_endpoint(self):
        response = self.client.get('/api/test')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "API is working"})

    @patch('app.routes.requests.get')
    def test_index_route_no_models(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = []
        
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No models currently running', response.data)

if __name__ == '__main__':
    unittest.main() 