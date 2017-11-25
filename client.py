from a_client.client_main import MyMessClient
from c_gui.start_form import MyGui

'''
Главный скрипт для старта клиента
'''
if __name__ == '__main__':
    # Коннект к серверу происходит в __init__ при создании обьекта класса
    name = 'sax'
    print(name)
    client = MyMessClient(name)
    # gui = MyGui(name)
    #
    #
    #
    #
    # gui.start_gui()


    # Старт режима сообщений
    client.client_start()
    # client.disconnect()
