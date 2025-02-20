from greet.config import name


def greet(name):
    return print(f'Hello {name}')


def main():
    greet(name=name)

if __name__ == '__main__':
    main()