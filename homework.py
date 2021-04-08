import datetime as dt


class Calculator:

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today = dt.date.today()
        return sum(i.amount for i in self.records if i.date == today)

    def get_week_stats(self):
        today = dt.date.today()
        start_date = dt.date.today() - dt.timedelta(days=6)
        return sum(i.amount for i in self.records
                   if today >= i.date >= start_date)


class CashCalculator(Calculator):

    USD_RATE = 60.0
    EURO_RATE = 70.0
    RUB_RATE = 1

    currency_dict = {'usd': (USD_RATE, 'USD'),
                     'eur': (EURO_RATE, 'Euro'),
                     'rub': (RUB_RATE, 'руб')}

    def get_today_cash_remained(self, currency):

        today_stats = self.get_today_stats()
        today_left = self.limit - today_stats

        if today_left == 0:
            return f'Денег нет, держись'
        rate, currency_text = self.currency_dict[currency]
        today_left_converted = abs(today_left / rate)

        if today_left > 0:
            return f'На сегодня осталось {today_left_converted:.2f} {currency_text}'
        return f'Денег нет, держись: твой долг - {today_left_converted:.2f} {currency_text}'


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        pass


class Record:

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()

    def __str__(self):
        return f'Деньги: {self.amount}, Комментарий: {self.comment}, Дата: {self.date}'


if __name__ == '__main__':
    # создадим калькулятор денег с дневным лимитом 1000
    cash_calculator = CashCalculator(1000)

    # дата в параметрах не указана,
    # так что по умолчанию к записи должна автоматически добавиться сегодняшняя дата
    #cash_calculator.add_record(Record(amount=145, comment="кофе"))
    # и к этой записи тоже дата должна добавиться автоматически
    #cash_calculator.add_record(Record(amount=300, comment="Серёге за обед"))
    # а тут пользователь указал дату, сохраняем её
    #cash_calculator.add_record(Record(amount=3000, comment="бар в Танин др", date="08.11.2019"))

    print(cash_calculator.get_today_cash_remained("rub"))
    #print(cash_calculator.get_week_stats())

    # должно напечататься
    # На сегодня осталось 555 руб
