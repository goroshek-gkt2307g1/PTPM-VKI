import unittest
import sys
import os
from unittest.mock import Mock
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from Database import Database
from Validators import Validators
from Controller import Controller
from UserInput import UserInput
from Notifier import Notifier

#заглушки
class MockUserInput(UserInput):
    def __init__(self, login, password, confPassword):
        self.login = login
        self.password = password
        self.confPassword = confPassword

    def getData(self):
        return self.login, self.password, self.confPassword

class MockNotifier(Notifier):
    def __init__(self):
        self.messages = []

    def send(self, message):
        self.messages.append(message)


#тесты
class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.db = Database(":memory:")
        self.validators = Validators()
        self.notifier = MockNotifier()
        self.blacklist = ["my_login"]

    def tearDown(self):
        self.db.close()

    #интгр: успешн рег
    def test_successful_registration(self):
        user_input = MockUserInput("good_login", "Пароль123!", "Пароль123!")
        controller = Controller(self.db, self.validators, user_input, self.notifier, self.blacklist)
        
        result = controller.run()
        
        self.assertEqual(result, "Success")
        self.assertEqual(self.notifier.messages[0], "Success")
        
        record = self.db.get("good_login", "Пароль123!", "Пароль123!")
        self.assertIsNotNone(record)
        self.assertEqual(str(record[0]), '1')

    #интегр: ошибка валидации
    def test_error_registration(self):
        user_input = MockUserInput("bad", "Пароль123!", "Пароль123!")
        controller = Controller(self.db, self.validators, user_input, self.notifier, self.blacklist)
        
        result = controller.run()
        
        self.assertEqual(result, "Error: Логин короче 5 символов")
        self.assertEqual(self.notifier.messages[0], "Error: Логин короче 5 символов")
        
        record = self.db.get("bad", "Пароль123!", "Пароль123!")
        self.assertIsNotNone(record)

    #интегр: данные берутся из БД (валидатор не вызывается)
    def test_caching_from_db(self):
        #вручную кладем запись в БД
        self.db.addReg("cached_login", "Пароль123!", "Пароль123!", True, "")
        
        mock_validator = Mock()
        user_input = MockUserInput("cached_login", "Пароль123!", "Пароль123!")
        
        #передаем mock_validator вместо настоящего
        controller = Controller(self.db, mock_validator, user_input, self.notifier, self.blacklist)
        result = controller.run()
        
        self.assertEqual(result, "Success")
        # Проверяем, что валидатор НЕ вызывался (взяли из кэша)
        mock_validator.check.assert_not_called()

    #юнит: удаление из бд
    def test_db_delete(self):
        self.db.addReg("del_login", "1", "1", True, "")
        self.db.delete("del_login", "1", "1")
        
        record = self.db.get("del_login", "1", "1")
        self.assertIsNone(record)

    #юнит: доб и получение
    def test_db_add_and_get(self):
        self.db.addReg("t", "1", "1", False, "Error")
        record = self.db.get("t", "1", "1")
        
        self.assertIsNotNone(record)
        self.assertEqual(record[1], "Error")

if __name__ == '__main__':
    unittest.main()