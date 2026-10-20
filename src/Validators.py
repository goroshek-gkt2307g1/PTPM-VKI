import logging
import sys
import re
import hashlib

#результат
class Result:
    def __init__(self, success, text):
        self.res = success
        self.message = text

    @staticmethod 
    def success():
        return Result(True, "")

    @staticmethod 
    def error(text):
        return Result(False, text)  

class Mask:
    @staticmethod
    def CreateHash(password):
        h = hashlib.sha256(password.encode("utf-8")).hexdigest()
        return "****" + h[:8]


#классификация логина
class ClassificationLogin:
    @staticmethod
    def findClass(login):
        result = ""
        patternNumber = r"^\+\d{1}-\d{3}-\d{3}-\d{4}$"
        patternEmail = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

        if re.match(patternNumber, login): 
            result = "number"
        elif re.match(patternEmail, login):
            result = "email"
        else:
            result = "stroka"
        return result

class Validators:
    def check(self, login, password, confPassword, blackList): #проверяет все
        result = self.checkLogin(login, blackList)
        if not result.res:
            return result

        result = self.checkPassword(password)
        if not result.res:
            return result

        result = self.checkMatch(password, confPassword)
        if not result.res:
            return result

        return Result.success()


    def checkLogin(self, login, blackList): #проверяет логин
        check = ClassificationLogin.findClass(login)

        if check == "":
            return Result.error("Логин пустой")

        if check == "stroka":
            if len(login) < 5:
                return Result.error("Логин короче 5 символов") 
            if not re.fullmatch(r"[A-Za-z0-9_]+", login):
                return Result.error("Логин: есть недопустимые символы")

        for item in blackList:
            if item == login:
                return Result.error("Логин в черном списке")

        return Result.success()

    def checkPassword(self, password): #проверяет пароль
        #7 символов, латиница, цифры, спецсимволы
        pattern = r"^[А-Яа-я0-9!\"#$%&'()*+,-./:;<=>?@[\\\]^_`{|}~]{7,}$"

        if len(password) < 7:
            return Result.error("Короткий пароль")

        if not re.match(pattern, password):
            return Result.error("Пароль: строка содержит запрещенные символы")

        if not re.search(r"[А-Я]", password):
            return Result.error("Пароль: нет заглавных букв")
        if not re.search(r"[а-я]", password):
            return Result.error("Пароль: нет прописных букв")
        if not re.search(r"[0-9]", password):
            return Result.error("Пароль: нет цифр")
        if not re.search(r"[^А-Яа-я0-9]", password): #проверяем все, кроме спецсимволов
            return Result.error("Пароль: нет спецсимволов")
        
        return Result.success()
    
    def checkMatch(self, password, confPassword): #проверяет свопадения паролей        
        if password == confPassword:
            return Result.success()
        else:
            return Result.error("Пароли не совпадают")