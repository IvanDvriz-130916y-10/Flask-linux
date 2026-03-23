import os
import random
import re
from datetime import datetime, timedelta

from flask import Flask

# Данные которые не меняются
AVAILABLE_CARS = ["Chevrolet", "Renault", "Ford", "Lada"]

CAT_BREEDS = [
    "корниш-рекс",
    "русская голубая",
    "шотландская вислоухая",
    "мейн-кун",
    "манчкин",
]

# Путь к файлу чтобы не зависеть от текущей директории
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
WAR_AND_PEACE_PATH = os.path.join(CURRENT_DIR, "war_and_peace.txt")

# Глобальный счётчик визитов
visits_counter = 0

# Слова из книги загружаем один раз при старте
def _extract_words_from_file(filepath):
    """Вытаскивает все слова из текста, отбрасывая знаки препинания."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            raw_text = f.read()
    except FileNotFoundError:
        # Если файла нет заглушка
        return ["слово", "книга", "мир", "война"]

# Заменяем всё кроме букв на пробелы
    cleaned = re.sub(r"[^а-яА-Яa-zA-Z\s]", " ", raw_text)
# Разбиваем и убираем пустые строки
    return [w for w in cleaned.split() if w]

BOOK_WORDS = _extract_words_from_file(WAR_AND_PEACE_PATH)

# Flask приложение
app = Flask(__name__)

@app.route("/hello_world")
def hello():
    """Самый простой эндпоинт."""
    return "Привет, мир!"

@app.route("/cars")
def list_cars():
    """Возвращает список машин через запятую."""
    return ", ".join(AVAILABLE_CARS)

@app.route("/cats")
def random_cat():
    """Случайная порода кошки."""
    return random.choice(CAT_BREEDS)

@app.route("/get_time/now")
def now_time():
    """Текущее время в читаемом формате."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"Сейчас {now}"

@app.route("/get_time/future")
def future_time():
    """Время через час."""
    later = (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
    return f"Через час будет {later}"

@app.route("/get_random_word")
def random_word():
    """Случайное слово из 'Войны и мира'."""
    return random.choice(BOOK_WORDS)

@app.route("/counter")
def counter():
    """Счётчик обращений к этому эндпоинту."""
    global visits_counter
    visits_counter += 1
    return str(visits_counter)

if __name__ == "__main__":
# Запускаем в режиме отладки
    app.run(debug=True)