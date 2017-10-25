from messenger import *

if __name__ == '__main__':
    # Коннект к серверу происходит в __init__ при создании обьекта класса
    client = MyMessClient()
    # Старт режима сообщений
    client.client_start()
