from rest_framework.test import APITestCase, APIClient
from unittest.mock import patch, MagicMock

class TestViews (APITestCase):
    def test_wikipedia_based_title(self):
        client = APIClient()
        response = client.get('/api/wikipedia/¡07734')
        self.assertEqual(response.status_code, 500)

    
    @patch('requests.get')   
    def test_wikipedia_based_extern_api(self, mock_get):
        mock_get.return_value.status_code = 500
        client = APIClient()
        response = client.get('/api/wikipedia/Rick_Astley')
        self.assertEqual(response.status_code, 500)
        
    
    @patch('requests.get')
    def test_wikipedia_based_short_word(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'parse': {
                'text': {'*': '<p>This is a test summary without long words like cat and dog cat sky.</p>'}
            }
        }
        mock_get.return_value = mock_response
        client = APIClient()
        response = client.get('/api/wikipedia/Rick_Astley')

        self.assertEqual(response.status_code, 200)
        data = response.data
        
        self.assertTrue(isinstance(data['mail sent'], bool))
        self.assertTrue(isinstance(data['long word'], int))
        self.assertTrue(isinstance(data['text'], str))
        self.assertTrue(isinstance(data['words list'], list))
        self.assertTrue(all(not" " in word for word in data['words list']))
        self.assertFalse(data['mail sent'])
        self.assertTrue(data['long word']<20.00)
        
        
    def test_wikipedia_based_type_test(self):
        client = APIClient()
        response = client.get('/api/wikipedia/Kaamelott')
        self.assertEqual(response.status_code, 200)
        data = response.data
        
        self.assertTrue(isinstance(data['mail sent'], bool))
        self.assertTrue(isinstance(data['long word'], int))
        self.assertTrue(isinstance(data['text'], str))
        self.assertTrue(isinstance(data['words list'], list))
        self.assertTrue( all(not" " in word for word in data['words list']))
        self.assertTrue(data['mail sent'])
        self.assertTrue(data['long word']>20.00)
        
        
        
        