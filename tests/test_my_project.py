import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from my_project import Validators, Result, Mask, ClassificationLogin

class TestRegistry(unittest.TestCase):
    def setUp(self):
        self.valid = Validators()
        self.blacklist = ["my_login", "+7-913-111-2233"]

    """"Проверки логина"""
    def test_empty_login(self):
        result = self.valid.checkLogin("", self.blacklist)
        self.assertFalse(result.res)
        self.assertEqual(result.message, "Логин пустой")

    def test_login_less_than_5(self):
        result = self.valid.checkLogin("haha", self.blacklist)
        self.assertFalse(result.res)
        self.assertEqual(result.message, "Логин короче 5 символов")

    def test_login_invalid_character(self):
        result = self.valid.checkLogin("lolkek!!!", self.blacklist)
        self.assertFalse(result.res)
        self.assertEqual(result.message, "Логин: есть недопустимые символы")

    def test_login_in_blacklist(self):
        result = self.valid.checkLogin("my_login", self.blacklist)
        self.assertFalse(result.res)
        self.assertEqual(result.message, "Логин в черном списке")

    """"Проверки пароля"""
    def test_less_than_7(self):
        result = self.valid.checkPassword("Хахаха")
        self.assertFalse(result.res)
        self.assertEqual(result.message, "Короткий пароль")

    def test_pass_invalid_character(self):
        result = self.valid.checkPassword("Hahahah")
        self.assertFalse(result.res)
        self.assertEqual(result.message, "Пароль: строка содержит запрещенные символы")

    def test_pass_no_up_character(self):
        result = self.valid.checkPassword("хахаха123!")
        self.assertFalse(result.res)
        self.assertEqual(result.message, "Пароль: нет заглавных букв")

    def test_pass_no_down_character(self):
        result = self.valid.checkPassword("ХАХАХА123!")
        self.assertFalse(result.res)
        self.assertEqual(result.message, "Пароль: нет прописных букв")

    def test_pass_no_digits(self):
        result = self.valid.checkPassword("Лалалала!")
        self.assertFalse(result.res)
        self.assertEqual(result.message, "Пароль: нет цифр")

    def test_pass_no_special_character(self):
        result = self.valid.checkPassword("Пупупу123")
        self.assertFalse(result.res)
        self.assertEqual(result.message, "Пароль: нет спецсимволов")

    """"Проверка совпадения паролей"""
    def test_pass_not_match(self):
        result = self.valid.checkMatch("Хахаха123!", "Хахаха123")
        self.assertFalse(result.res)
        self.assertEqual(result.message, "Пароли не совпадают")

if __name__ == '__main__':
    unittest.main()
