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

#правила/валидация
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
        if login == "":
            return Result.error("Логин пустой")
        
        check = ClassificationLogin.findClass(login)


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

#логи
class Logs:
    def createLogging(self):
        log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
        date_format = "%Y-%m-%d %H:%M:%S"

    # Базовая настройка корневого логгера
        logging.basicConfig(
            level=logging.DEBUG, # Минимальный уровень логирования (аналог MinimumLevel.Debug)
            format=log_format,
            datefmt=date_format,
            handlers=[
                logging.StreamHandler(sys.stdout),          # Настройка логирования в консоль
                logging.FileHandler("logs/file_txt.log", encoding="utf-8") # Настройка логирования в файл
            ]
        )

        logging.info("Логгер успешно сконфигурирован")
        logging.info("Приложение запущено")

class Mask:
    @staticmethod
    def CreateHash(password):
        h = hashlib.sha256(password.encode("utf-8")).hexdigest()
        return "****" + h[:8]

#точка входа
def main():
    blackList = ["+7-900-900-1234", "haha@gmail.com", "my_login"]

    logs = Logs()
    logs.createLogging()

    login = input("Введите логин: ")
    password = input("Введите пароль: ")
    confPassword = input("Подтвердите пароль: ")

    validator = Validators()

    try:
        result = validator.check(login, password, confPassword, blackList)

        if result.res:
            print("Успех")
            logging.info("Success: login=%s, password=%s, confirm password=%s", login, Mask.CreateHash(password), Mask.CreateHash(confPassword))
        else:
            print("Ошибка: ", result.message)
            logging.warning("Error: login=%s, password=%s, confirm password=%s, message=%s", login, Mask.CreateHash(password), Mask.CreateHash(confPassword), result.message)

    except Exception:
        logging.exception("Сбой при регистрации")
        print("Error: внутренняя ошибка")
        return

if __name__ == "__main__": main()