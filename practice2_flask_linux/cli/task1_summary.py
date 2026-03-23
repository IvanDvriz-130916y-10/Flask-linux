import sys
import os

# Список единиц измерения памяти
units = ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB']


def format_bytes(byte_count):
    """
    Переводит количество байт в удобочитаемый вид.
    """
    if byte_count < 0:
        return f"{byte_count} B"
    size = float(byte_count)
    idx = 0
# Пока число больше 1023 и есть более крупная единица происходит переход
    while size >= 1024.0 and idx < len(units) - 1:
        size /= 1024.0
        idx += 1
# Если результат целый выводим без десятичных знаков
    if size.is_integer():
        return f"{int(size)} {units[idx]}"
    else:
        return f"{size:.2f} {units[idx]}"


def read_ps_aux(file_path):
    """
    Читает файл с выводом команды ps aux, суммирует RSS (6-й столбец).
    Возвращает итоговое число байт.
    """
    total = 0
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
# Пропускаем первую строку
            first = True
            for line in f:
                if first:
                    first = False
                    continue
# Разбиваем строку по пробельным символам
                parts = line.split()
                if len(parts) < 6:
                    continue
                try:
# RSS шестое поле (индекс 5)
                    rss = int(parts[5])
                    total += rss
                except ValueError:
# Если поле не число пропускаем строку
                    continue
    except FileNotFoundError:
        sys.stderr.write(f"Ошибка: файл '{file_path}' не найден.\n")
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(f"Ошибка при чтении файла: {e}\n")
        sys.exit(1)
    return total


def main():
    if len(sys.argv) != 2:
        print("Использование: python3 script.py <файл_ps_aux>")
        sys.exit(2)

    ps_file = sys.argv[1]
    if not os.path.isfile(ps_file):
        sys.stderr.write(f"Файл '{ps_file}' не существует.\n")
        sys.exit(1)

    total_bytes = read_ps_aux(ps_file)
    print(format_bytes(total_bytes))


if __name__ == "__main__":
    main()