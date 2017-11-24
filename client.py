from a_client.client_main import MyMessClient
# from sqlalchemy.ext.declarative import declarative_base
# from b_server.db.server_db_def import ServerDbControl
# Base = declarative_base()

'''
Главный скрипт для старта клиента
'''
if __name__ == '__main__':
    # Коннект к серверу происходит в __init__ при создании обьекта класса
    name = 'sax'
    print(name)
    client = MyMessClient(name)
    # Добавляет клиентов для тестов
    # client.db.add_user('Test2')
    # client.db.add_user('Test3')
    # client.db.add_user('Test4')
    # client.db.add_user('Test5')
    # client.db.commit()

    # server = ServerDbControl('server.db', 'b_server/db', Base)
    # server.add_client('Test6')
    # server.add_client('Test7')
    # server.add_client('Test8')
    # server.add_client('Test9')
    # server.add_client('Test10')
    # server.commit()
    # Старт режима сообщений
    client.client_start()
    client.disconnect()
