from .UserInput import UserInput

class ConsoleInput(UserInput):
    def getData(self):
        login = input("Введите логин: ")
        password = input("Введите пароль: ")
        confPassword = input("Подтвердите пароль: ")
        return login, password, confPassword