import unittest
import os
from src.parser import ForumParser
from src.DatabaseRepository import DatabaseRepository

class TestForumParser(unittest.TestCase):
    def setUp(self):
        self.parser = ForumParser()
        #путь к файлу
        self.fixture_path = os.path.join(
            os.path.dirname(__file__), 'code_html', 'test_code.html'
        )

    def test_parse_html(self):
        #читаем HTML
        with open(self.fixture_path, 'r', encoding='windows-1251') as f: #гарантирует закрытие файла даже при ошибке
            html = f.read()

        #парсим
        result = self.parser.parse_html(html)

        #проверка, что нашли посты
        self.assertGreater(len(result), 0, "Парсер не нашел ни одного поста")
        
        #проверяем первый пост
        first = result[0]
        self.assertEqual(first['id'], 4847640)
        self.assertEqual(first['name'], '_Woland_')
        self.assertIn('Вопросы новичка', first['message'])

    def test_save_to_db(self):
        db = DatabaseRepository(':memory:')
        parsed = [{'id': 1, 'name': 'User', 'message': 'Text'}]
        count = self.parser.save_to_db(parsed, db)
        self.assertEqual(count, 1)
        self.assertIsNotNone(db.get_by_id(1))
        db.close()

if __name__ == '__main__':
    unittest.main()