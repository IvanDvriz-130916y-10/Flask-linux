import sys

def main():
# Читаем всё что пришло на стандартный ввод
    data = sys.stdin.read()
    
# Разбиваем на строки
    lines = data.splitlines()
    
    total_size = 0
    file_count = 0
    
# Проходим по каждой строке
    for line in lines:
        # Пропускаем пустые строки
        if not line.strip():
            continue
        
# Строка начинающаяся с "total" это не файл а статистика
        if line.startswith('total'):
            continue
        
# Разделяем строку по пробелам
# Используем maxsplit=8 чтобы имя файла которое может содержать пробелы не испортило разбор
        parts = line.split(maxsplit=8)
        if len(parts) < 5:
# Если полей меньше 5 строка нам не подходит
            continue
        
# Первое поле права доступа
# Нас интересуют только обычные файлы у них первый символ '-'
        permissions = parts[0]
        if not permissions.startswith('-'):
# Каталог, ссылка или специальный файл — пропускаем
            continue
        
# Пятое поле (индекс 4)
        try:
            size = int(parts[4])
        except ValueError:
# Если размер не число игнорируем строку
            continue
        
        total_size += size
        file_count += 1
    
    if file_count == 0:
# Нет обычных файлов среднее 0
        mean_size = 0.0
    else:
        mean_size = total_size / file_count
    
# Выводим результат если целое число то без дробной части иначе с двумя знаками
    if abs(mean_size - int(mean_size)) < 1e-9:
        print(int(mean_size))
    else:
        print(f"{mean_size:.2f}")

if __name__ == "__main__":
    main()