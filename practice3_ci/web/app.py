"""Flask endpoints — практика 2/3. Тот же функционал, но в другом стиле."""

from datetime import datetime
from pathlib import Path
from flask import Flask, Response
from .greetings import get_username_with_weekdate

app = Flask(__name__)

PROJ_ROOT = Path(__file__).resolve().parent.parent


# хранилище расходов
class MoneyStorage:
    def __init__(self):
        self.daily = {}
        self.monthly = {}
        self.yearly = {}

    def clear(self):
        self.daily.clear()
        self.monthly.clear()
        self.yearly.clear()

    def add(self, date_str, amount):
        year = int(date_str[:4])
        month = int(date_str[4:6])

# дневная сумма
        self.daily[date_str] = self.daily.get(date_str, 0) + amount
    # месячная
        key = (year, month)
        self.monthly[key] = self.monthly.get(key, 0) + amount
# годовая
        self.yearly[year] = self.yearly.get(year, 0) + amount

        return self.daily[date_str]


storage = MoneyStorage()


@app.get("/")
def index():
    html = """<h2>Practice 2/3: Flask endpoints</h2>
<ul>
  <li>/hello-world/&lt;name&gt;</li>
  <li>/max_number/&lt;numbers separated by /&gt; (пример: /max_number/10/2/9/1)</li>
  <li>/preview/&lt;size&gt;/&lt;relative_path&gt; (пример: /preview/8/docs/simple.txt)</li>
  <li>/add/&lt;YYYYMMDD&gt;/&lt;amount&gt; (пример: /add/20260214/150)</li>
  <li>/calculate/&lt;year&gt; (пример: /calculate/2026)</li>
  <li>/calculate/&lt;year&gt;/&lt;month&gt; (пример: /calculate/2026/2)</li>
</ul>
"""
    return Response(html, mimetype="text/html; charset=utf-8")


@app.get("/hello-world/<name>")
def hello_world(name):
    text = get_username_with_weekdate(name)
    return Response(text, mimetype="text/plain; charset=utf-8")


@app.get("/max_number/<path:numbers>")
def max_number(numbers):
    parts = [p for p in numbers.split("/") if p]  # убираем пустые
    if not parts:
        return Response("Ошибка: не переданы числа.", status=400, mimetype="text/plain; charset=utf-8")

    nums = []
    for p in parts:
        try:
            nums.append(int(p))
        except ValueError:
            return Response(
                f"Ошибка: '{p}' не является целым числом.",
                status=400,
                mimetype="text/plain; charset=utf-8",
            )

    max_val = max(nums)
    return Response(f"Максимальное число: <i>{max_val}</i>", mimetype="text/html; charset=utf-8")


@app.get("/preview/<int:size>/<path:relative_path>")
def preview(size, relative_path):
    if size < 0:
        return Response("Ошибка: SIZE должен быть неотрицательным.", status=400, mimetype="text/plain; charset=utf-8")

    target = (PROJ_ROOT / relative_path).resolve()
    base = PROJ_ROOT.resolve()

# защита от обхода папок
    try:
        target.relative_to(base)
    except ValueError:
        return Response("Ошибка: доступ к пути запрещён.", status=403, mimetype="text/plain; charset=utf-8")

    if not target.is_file():
        return Response("Ошибка: файл не найден.", status=404, mimetype="text/plain; charset=utf-8")

    try:
        with open(target, "r", encoding="utf-8", errors="replace") as f:
            preview_text = f.read(size)
    except Exception as e:
        return Response(f"Ошибка чтения: {e}", status=500)

    return Response(f"<b>{target}</b> {len(preview_text)}<br>{preview_text}", mimetype="text/html; charset=utf-8")


@app.get("/add/<date>/<int:number>")
def add_expense(date, number):
# если дата невалидна упадёт в тестах
    datetime.strptime(date, "%Y%m%d")
    day_total = storage.add(date, number)
    return Response(
        f"Добавлено {number} руб. за {date}. Итого за день: {day_total} руб.",
        mimetype="text/plain; charset=utf-8",
    )


@app.get("/calculate/<int:year>")
def calculate_year(year):
    total = storage.yearly.get(year, 0)
    return Response(f"Суммарные траты за {year} год: {total} руб.", mimetype="text/plain; charset=utf-8")


@app.get("/calculate/<int:year>/<int:month>")
def calculate_month(year, month):
    if month < 1 or month > 12:
        return Response("Ошибка: month должен быть от 1 до 12.", status=400, mimetype="text/plain; charset=utf-8")
    total = storage.monthly.get((year, month), 0)
    return Response(f"Суммарные траты за {year}-{month:02d}: {total} руб.", mimetype="text/plain; charset=utf-8")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)