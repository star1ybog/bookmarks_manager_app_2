import unittest
import json
from app import app

class APITestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.headers = {'Content-Type': 'application/json'}

    # Тест для головної сторінки
    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Bookmarks Manager', response.data)

    # Тест на створення закладки (позитивний)
    def test_create_bookmark(self):
        new_bookmark = {
            'title': 'Example Bookmark',
            'url': 'http://example.com',
            'category': 'Programming'
        }
        response = self.app.post('/bookmark', data=json.dumps(new_bookmark), headers=self.headers)
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Example Bookmark', response.data)

    # Негативний тест на дублювання URL
    def test_create_duplicate_bookmark(self):
        duplicate_bookmark = {
            'title': 'Duplicate Bookmark',
            'url': 'http://example.com',
            'category': 'Programming'
        }
        self.app.post('/bookmark', data=json.dumps(duplicate_bookmark), headers=self.headers)
        response = self.app.post('/bookmark', data=json.dumps(duplicate_bookmark), headers=self.headers)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Bookmark already exists!', response.data)

    # Тест на отримання існуючої закладки (позитивний)
    def test_get_bookmark(self):
        new_bookmark = {
            'title': 'Test Bookmark',
            'url': 'http://test.com',
            'category': 'Tests'
        }
        create_response = self.app.post('/bookmark', data=json.dumps(new_bookmark), headers=self.headers)
        bookmark_id = json.loads(create_response.data)['id']
        
        get_response = self.app.get(f'/bookmark/{bookmark_id}')
        self.assertEqual(get_response.status_code, 200)
        self.assertIn(b'Test Bookmark', get_response.data)

    # Тест на отримання неіснуючої закладки (негативний)
    def test_get_non_existent_bookmark(self):
        response = self.app.get('/bookmark/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'404', response.data)

    # Тест на редагування закладки (позитивний)
    def test_edit_bookmark(self):
        new_bookmark = {
            'title': 'Initial Title',
            'url': 'http://initial.com',
            'category': 'Tests'
        }
        create_response = self.app.post('/bookmark', data=json.dumps(new_bookmark), headers=self.headers)
        bookmark_id = json.loads(create_response.data)['id']

        updated_bookmark = {
            'title': 'Updated Title',
            'url': 'http://updated.com',
            'category': 'Updated'
        }
        edit_response = self.app.put(f'/bookmark/{bookmark_id}', data=json.dumps(updated_bookmark), headers=self.headers)
        self.assertEqual(edit_response.status_code, 200)
        self.assertIn(b'Updated Title', edit_response.data)

    # Тест на редагування неіснуючої закладки (негативний)
    def test_edit_non_existent_bookmark(self):
        updated_bookmark = {
            'title': 'Non-existent Title',
            'url': 'http://nonexistent.com',
            'category': 'None'
        }
        response = self.app.put('/bookmark/999', data=json.dumps(updated_bookmark), headers=self.headers)
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Bookmark not found', response.data)

    # Тест на видалення закладки (позитивний)
    def test_delete_bookmark(self):
        new_bookmark = {
            'title': 'To be deleted',
            'url': 'http://delete.com',
            'category': 'Tests'
        }
        create_response = self.app.post('/bookmark', data=json.dumps(new_bookmark), headers=self.headers)
        bookmark_id = json.loads(create_response.data)['id']

        delete_response = self.app.delete(f'/bookmark/{bookmark_id}')
        self.assertEqual(delete_response.status_code, 200)
        self.assertIn(b'Bookmark deleted', delete_response.data)

    # Тест на видалення неіснуючої закладки (негативний)
    def test_delete_non_existent_bookmark(self):
        response = self.app.delete('/bookmark/999')
        self.assertEqual(response.status_code, 200)  # Тут може бути 200, бо видалення неіснуючої закладки теж успішне
        self.assertIn(b'Bookmark deleted', response.data)

if __name__ == '__main__':
    unittest.main()
