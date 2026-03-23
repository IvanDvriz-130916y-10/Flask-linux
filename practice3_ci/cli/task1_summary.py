import sys
import os

# единицы измерения размера памяти
UNITS = ["B", "KiB", "MiB", "GiB", "TiB", "PiB"]

def format_bytes(byte_count):
    """
    Переводит байты в читаемый вид.
    """
    if byte_count < 0:
        return f"{byte_count} B"
    value = float(byte_count)
    idx = 0
    while value >= 1024.0 and idx < len(UNITS) - 1:
        value /= 1024.0
        idx += 1
# если число целое без дробной части
    if value.is_integer():
        return f"{int(value)} {UNITS[idx]}"
    else:
        return f"{value:.2f} {UNITS[idx]}"


def get_total_rss(file_path):
    """
    Читает файл с выводом ps aux, суммирует RSS (6-й столбец).
    Возвращает сумму в байтах.
    """
    total = 0
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
# пропускаем первую строку
            first_line = True
            for line in f:
                if first_line:
                    first_line = False
                    continue
                line = line.strip()
                if not line:
                    continue
                cols = line.split()
# ожидаем как минимум 6 полей
                if len(cols) < 6:
                    continue
# шестое поле RSS
                try:
                    rss = int(cols[5])
                except ValueError:
                    continue
                total += rss
    except Exception as e:
        sys.stderr.write(f"Ошибка при чтении файла: {e}\n")
        sys.exit(1)
    return total


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python3 script.py <файл_ps_aux>")
        sys.exit(2)

    path = sys.argv[1]
    if not os.path.isfile(path):
        sys.stderr.write(f"Файл '{path}' не существует.\n")
        sys.exit(1)

    total_bytes = get_total_rss(path)
    print(format_bytes(total_bytes))