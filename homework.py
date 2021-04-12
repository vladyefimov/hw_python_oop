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

    def get_today_left(self):
        return self.limit - self.get_today_stats()

    def get_week_stats(self):
        today = dt.date.today()
        start_date = dt.date.today() - dt.timedelta(days=6)
        return sum(i.amount for i in self.records
                   if today >= i.date >= start_date)


class CashCalculator(Calculator):

    USD_RATE = 70.0
    EURO_RATE = 80.0
    RUB_RATE = 1

    def get_today_cash_remained(self, currency):

        currency_dict = {'usd': (self.USD_RATE, 'USD'),
                         'eur': (self.EURO_RATE, 'Euro'),
                         'rub': (self.RUB_RATE, 'руб')}

        today_left = self.get_today_left()

        if today_left == 0:
            return f'Денег нет, держись'

        rate, currency_text = currency_dict[currency]
        today_left_converted = abs(today_left / rate)

        if today_left > 0:
            return f'На сегодня осталось {today_left_converted:.2f} {currency_text}'
        return f'Денег нет, держись: твой долг - {today_left_converted:.2f} {currency_text}'


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        today_left = self.get_today_left()

        if today_left <= 0:
            return f'Хватит есть!'
        elif today_left > 0:
            return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {today_left} кКал'


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
    # creates cash calculator with day limit of 1000
    cash_calculator = CashCalculator(1000)
    # adds record without data,
    # so should be added current date by default
    cash_calculator.add_record(Record(amount=145, comment="кофе"))
    # and for this one too should be added current date
    cash_calculator.add_record(Record(amount=300, comment="Серёге за обед"))
    # date in this record should be added as date in date format
    cash_calculator.add_record(Record(amount=3000, comment="бар в Танин др", date="08.11.2019"))

    print(cash_calculator.get_today_cash_remained("rub"))

    # should be printed
    # На сегодня осталось 555 руб
