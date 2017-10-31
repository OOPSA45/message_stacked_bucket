import sys
from server.main import MyMessServer

# from messenger import *

if __name__ == '__main__':
    print('Запускаю сервер')
    # Получаем аргументы скрипта
    try:
        addr = sys.argv[1]
    except IndexError:
        addr = ''
    try:
        port = int(sys.argv[2])
    except IndexError:
        port = 7777
    except ValueError:
        print('Порт должен быть целым числом')
        sys.exit(0)

    server = MyMessServer(addr, port)
    server.main_loop()
