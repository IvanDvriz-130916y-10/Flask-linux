import datetime

class Person:
    """Класс для представления человека с именем, годом рождения и адресом."""

    def __init__(self, name, year_of_birth, address=""):
# запоминаем данные
        self.name = name
        self.year = year_of_birth
        self.addr = address

    def get_age(self):
# считаем возраст по текущему году
        now = datetime.date.today()
        return now.year - self.year

    def get_name(self):
        return self.name

    def set_name(self, new_name):
        self.name = new_name

    def get_address(self):
        return self.addr

    def set_address(self, new_address):
        self.addr = new_address

    def is_homeless(self):
# если адрес не задан или пустая строка бездомный
        if self.addr is None or self.addr == "":
            return True
        return False