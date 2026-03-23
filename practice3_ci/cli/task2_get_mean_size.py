import sys

def main():
# Читаем всё что пришло на стандартный ввод
    text = sys.stdin.read()
    rows = text.splitlines()

    total = 0
    count = 0

    for row in rows:
        row = row.strip()
        if not row:
            continue

# Пропускаем служебную строку
        if row.startswith('total'):
            continue

# Разбиваем строку на поля максимум 9 частей
        fields = row.split(maxsplit=8)
        if len(fields) < 5:
            continue

# Права доступа обычный файл начинается с '-'
        if fields[0][0] != '-':
            continue

        try:
            size = int(fields[4])
        except ValueError:
            continue

        total += size
        count += 1

    if count == 0:
        avg = 0.0
    else:
        avg = total / count

# Если среднее целое выводим без дробной части
    if avg == int(avg):
        print(int(avg))
    else:
        print(f"{avg:.2f}")

if __name__ == "__main__":
    main()