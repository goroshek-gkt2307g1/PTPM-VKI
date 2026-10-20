from .Notifier import Notifier

class EmailNotifier(Notifier):
    def send(self, message):
        print(f"Отправка на почту: {message}")