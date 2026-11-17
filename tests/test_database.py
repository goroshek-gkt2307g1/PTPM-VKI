import unittest
import sqlite3
from src.DatabaseRepository import DatabaseRepository


class TestDatabaseRepository(unittest.TestCase):
    def setUp(self): #перед каждым
        #база в памяти для каждого теста
        self.db = DatabaseRepository(':memory:')

    def tearDown(self): #после каждого
        self.db.close()

    #add
    def test_add_success(self):
        "Успешное добавление записи"
        self.assertTrue(self.db.add(1, "Alice", "Hello"))
        record = self.db.get_by_id(1)
        self.assertIsNotNone(record)
        self.assertEqual(record['id'], 1)
        self.assertEqual(record['name'], "Alice")
        self.assertEqual(record['message'], "Hello")

    def test_add_duplicate_id_raises(self):
        "Дубликат ID должен выбросить sqlite3.IntegrityError."
        self.db.add(1, "Alice", "Hello")
        with self.assertRaises(sqlite3.IntegrityError): #исключение бд при нарушении PK
            self.db.add(1, "Bob", "Duplicate")

    def test_add_invalid_message_length_raises(self):
        "Сообщение длиннее 8096 символов - ValueError"
        long_message = "x" * 8097
        with self.assertRaises(ValueError):
            self.db.add(1, "Alice", long_message)

    #get_by_id
    def test_get_by_id_exists(self):
        "Поиск существующей записи"
        self.db.add(1, "Alice", "Hello")
        record = self.db.get_by_id(1)
        self.assertIsNotNone(record)
        self.assertEqual(record['message'], "Hello")

    def test_get_by_id_not_exists(self):
        "Поиск несуществующей записи - None"
        self.assertIsNone(self.db.get_by_id(999))

    #get_by_name
    def test_get_by_name_returns_all(self):
        "Возвращает все записи пользователя"
        self.db.add(1, "Alice", "Msg1")
        self.db.add(2, "Alice", "Msg2")
        self.db.add(3, "Bob", "Msg3")
        records = self.db.get_by_name("Alice")
        self.assertEqual(len(records), 2)
        self.assertEqual({r['message'] for r in records}, {"Msg1", "Msg2"})

    def test_get_by_name_not_exists(self):
        "Нет записей - пустой список"
        records = self.db.get_by_name("Unknown")
        self.assertEqual(records, [])

    #update
    def test_update_success(self):
        "Успешное изменение сообщения"
        self.db.add(1, "Alice", "Old Text")
        self.assertTrue(self.db.update(1, "New Text"))
        self.assertEqual(self.db.get_by_id(1)['message'], "New Text")

    def test_update_not_exists(self):
        "Несуществующий ID - False"
        self.assertFalse(self.db.update(999, "New Text"))

    def test_update_invalid_length_raises(self):
        "Новое сообщение длиннее 8096 - ValueError"
        self.db.add(1, "Alice", "Old")
        with self.assertRaises(ValueError):
            self.db.update(1, "x" * 8097)

    #delete
    def test_delete_success(self):
        "Успешное удаление"
        self.db.add(1, "Alice", "To delete")
        self.assertTrue(self.db.delete(1))
        self.assertIsNone(self.db.get_by_id(1))

    def test_delete_not_exists(self):
        "Удаление несуществующего ID - False"
        self.assertFalse(self.db.delete(999))


if __name__ == '__main__':
    unittest.main()