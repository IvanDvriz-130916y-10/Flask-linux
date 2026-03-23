from datetime import datetime
from pathlib import Path

from flask import Flask, Response

app = Flask(__name__)

# Корень проекта вычисляем один раз при старте
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Дни недели
DAY_WISHES = [
    "Хорошего понедельника",
    "Хорошего вторника",
    "Хорошей среды",
    "Хорошего четверга",
    "Хорошей пятницы",
    "Хорошей субботы",
    "Хорошего воскресенья",
]

# Используем простые словари без обёртки в класс
daily_expenses = {}
monthly_expenses = {}
yearly_expenses = {}


def add_expense_record(date_str, amount):
    """Добавляет расход и обновляет агрегаты."""
# Извлекаем год и месяц из строки
    year = int(date_str[:4])
    month = int(date_str[4:6])

# Обновляем дневную сумму
    daily_expenses[date_str] = daily_expenses.get(date_str, 0) + amount

# Обновляем месячную
    key_month = (year, month)
    monthly_expenses[key_month] = monthly_expenses.get(key_month, 0) + amount

# Обновляем годовую
    yearly_expenses[year] = yearly_expenses.get(year, 0) + amount

    return daily_expenses[date_str]


# Endpoints
@app.route("/")
def index():
    html = """
    <h2>Flask: практика 2</h2>
    <ul>
      <li><code>/hello-world/&lt;имя&gt;</code></li>
      <li><code>/max_number/&lt;числа через /&gt;</code> (пример: /max_number/5/12/3)</li>
      <li><code>/preview/&lt;размер&gt;/&lt;относительный_путь&gt;</code> (пример: /preview/10/docs/readme.txt)</li>
      <li><code>/add/&lt;ГГГГММДД&gt;/&lt;сумма&gt;</code> (пример: /add/20260214/150)</li>
      <li><code>/calculate/&lt;год&gt;</code> (пример: /calculate/2026)</li>
      <li><code>/calculate/&lt;год&gt;/&lt;месяц&gt;</code> (пример: /calculate/2026/2)</li>
    </ul>
    """
    return Response(html, mimetype="text/html; charset=utf-8")


@app.route("/hello-world/<name>")
def hello_world(name):
# Получаем текущий день недели (0-6)
    today = datetime.today().weekday()
    wish = DAY_WISHES[today]
    return Response(f"Привет, {name}. {wish}!", mimetype="text/plain; charset=utf-8")


@app.route("/max_number/<path:numbers>")
def max_number(numbers):
    # Разбиваем строку по слешам, игнорируя пустые куски
    parts = [p for p in numbers.split('/') if p]
    if not parts:
        return Response("Ошибка: не переданы числа.", status=400, mimetype="text/plain; charset=utf-8")

    values = []
    for p in parts:
        try:
            values.append(int(p))
        except ValueError:
            return Response(f"Ошибка: '{p}' не является целым числом.", status=400, mimetype="text/plain; charset=utf-8")

    max_val = max(values)
    return Response(f"Максимальное число: <i>{max_val}</i>", mimetype="text/html; charset=utf-8")


@app.route("/preview/<int:size>/<path:relative_path>")
def preview(size, relative_path):
    if size < 0:
        return Response("Ошибка: размер должен быть неотрицательным.", status=400, mimetype="text/plain; charset=utf-8")

# Абсолютный путь к запрошенному файлу
    full_path = (PROJECT_ROOT / relative_path).resolve()
# Проверка что файл лежит внутри проекта
    try:
        full_path.relative_to(PROJECT_ROOT)
    except ValueError:
        return Response("Ошибка: доступ к файлу запрещён.", status=403, mimetype="text/plain; charset=utf-8")

    if not full_path.exists() or not full_path.is_file():
        return Response("Ошибка: файл не найден.", status=404, mimetype="text/plain; charset=utf-8")

# Читаем первые size символов
    try:
        with open(full_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read(size)
    except Exception as e:
        return Response(f"Ошибка чтения файла: {e}", status=500, mimetype="text/plain; charset=utf-8")

    return Response(f"<b>{full_path}</b> {len(content)}<br>{content}", mimetype="text/html; charset=utf-8")


@app.route("/add/<date>/<int:number>")
def add(date, number):
# Проверяем формат даты (YYYY MM DD)
    if len(date) != 8 or not date.isdigit():
        return Response("Ошибка: дата должна быть в формате YYYYMMDD.", status=400, mimetype="text/plain; charset=utf-8")
    try:
        datetime.strptime(date, "%Y%m%d")
    except ValueError:
        return Response("Ошибка: некорректная дата.", status=400, mimetype="text/plain; charset=utf-8")

    total = add_expense_record(date, number)
    return Response(f"Добавлено {number} руб. за {date}. Итого за день: {total} руб.", mimetype="text/plain; charset=utf-8")


@app.route("/calculate/<int:year>")
def calculate_year(year):
    total = yearly_expenses.get(year, 0)
    return Response(f"Суммарные траты за {year} год: {total} руб.", mimetype="text/plain; charset=utf-8")


@app.route("/calculate/<int:year>/<int:month>")
def calculate_month(year, month):
    if month < 1 or month > 12:
        return Response("Ошибка: месяц должен быть от 1 до 12.", status=400, mimetype="text/plain; charset=utf-8")
    total = monthly_expenses.get((year, month), 0)
    return Response(f"Суммарные траты за {year}-{month:02d}: {total} руб.", mimetype="text/plain; charset=utf-8")


if __name__ == "__main__":
# Запускаем встроенный сервер
    app.run(host="127.0.0.1", port=5000, debug=True)