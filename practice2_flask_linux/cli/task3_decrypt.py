import sys

def decrypt_string(s):
    """Расшифровывает строку: 
    . - пропускается, 
    .. - удаляет предыдущий символ"""
    res = []
    skip = False
    n = len(s)
    for i in range(n):
        if skip:
            skip = False
            continue
        ch = s[i]
        if ch == '.' and i+1 < n and s[i+1] == '.':
            if res:
                res.pop()
            skip = True
        elif ch != '.':
            res.append(ch)
# одиночную точку просто игнорируем
    return ''.join(res)

if __name__ == "__main__":
    data = sys.stdin.read()
    if data.endswith('\n'):
        data = data[:-1]
    print(decrypt_string(data))