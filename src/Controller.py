

class Controller:
    def __init__(self, db, validators, user_input, notifier, blackList):
        self.db = db
        self.validators = validators
        self.user_input = user_input
        self.notifier = notifier
        self.blacklist = blackList

    def run(self):
        login, password, confPassword = self.user_input.getData() #получ данные
        db_record = self.db.get(login, password, confPassword) #поиск в бд

        if db_record is not None: #есть в бд
            db_result = db_record[0]
            db_message = db_record[1]

        else: #нет в бд
            val_result = self.validators.check(login, password, confPassword, self.blacklist)
            db_result = val_result.res
            db_message = val_result.message

            self.db.addReg(login, password, confPassword, db_result, db_message)

        if str(db_result) in ('True', '1') or db_result is True:
            final_message = 'Success'

        else:
            final_message = f'Error: {db_message}'

        self.notifier.send(final_message)
        return final_message


    