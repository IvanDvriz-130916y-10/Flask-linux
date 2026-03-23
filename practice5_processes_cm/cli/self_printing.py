import sys

def print_self():
    with open(sys.argv[0], 'r', encoding='utf-8') as f:
        sys.stdout.write(f.read())

if __name__ == '__main__':
    print_self()