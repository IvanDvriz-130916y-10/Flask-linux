import sys

def decode(s):
    """Расшифровывает строку по правилам:
    . - удаляется
    .. - удаляет предыдущий символ (если есть)"""
    out = []
    i = 0
    L = len(s)
    while i < L:
        if s[i] == '.':
            if i+1 < L and s[i+1] == '.':
                if out:
                    out.pop()    # удаляем предыдущий символ
                i += 2           # пропускаем две точки
            else:
                i += 1           # пропускаем одну точку
        else:
            out.append(s[i])
            i += 1
    return ''.join(out)

if __name__ == '__main__':
    data = sys.stdin.read().strip('\n')   # убираем перевод строки если есть
    print(decode(data))