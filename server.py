# Основное задание:
# ● Реализовать логгирование с использованием модуля logging: +
#   ○ Реализовать декоратор @log, фиксирующий обращение к декорируемой функции:
#   сохраняет имя функции и её аргументы. +

#   ● Реализовать обработку нескольких клиентов на сервере с использованием
#   функции select таким образом, что клиенты общаются в "общем чате", т.е.
#   каждое сообщение каждого клиента отправляется всем клиентам,
#   подключенным к серверу.

#   ● Реализовать функции отправки/приёма данных на стороне клиента. Для
#   упрощения разработки приложения на данном этапе пусть клиентское
#   приложение будет либо только принимать, либо только отправлять сообщения в
#   общий чат:

#   ● запуск скрипта клиента должен осуществляться с параметром командной
#   строки: -r (чтение чата) или -w (передача сообщений в чат).

#   ● Для всех функций необходимо написать тесты.

from socket import *
import select
import time
import json
import logging
from functools import wraps

# Подключает настройки логирования
import log_config
LOG_LEVEL = logging.DEBUG
log_config.set_logger('server', LOG_LEVEL)
SERVER_LOG = logging.getLogger('server')

# ○ Реализовать декоратор @log, фиксирующий обращение к декорируемой функции:
# сохраняет имя функции и её аргументы. +
class Log:

    def __call__(self, func):
        @wraps(func)
        def inner(*args, **kwargs):
            result = func(*args, **kwargs)
            SERVER_LOG.debug('{}'.format(func.__name__))
            return result
        return inner


log = Log()


# Получает сообщение от клиента
@log
def get_presence(client):
    bpresence = client.recv(1024)
    jpresence = bpresence.decode('utf-8')
    presence = json.loads(jpresence)
    return presence


# Отправляет сообщение клиенту
@log
def send_response(response, client):
    jresponse = json.dumps(response)
    bresponse = jresponse.encode('utf-8')
    client.send(bresponse)


# Форматирует в JIM
@log
def response_format(response_code, time, alert,):
    response = {
        "response": response_code,
        "time": time,
        "alert": alert
    }
    return response


# Формирует ответ клиенту
@log
def presence_parse(presence_message):
    if presence_message['action'] == 'presence':
        response_message = response_format('200', time.time(), 'Presence well done! :: ' + time.ctime(presence_message['time']))
    else:
        response_message = response_format('400', time.time(), 'Unknown query :: ' + time.ctime(presence_message['time']))
    return response_message


@log
def new_listen_socket(address):
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(address)
    s.listen(5)
    s.settimeout(0.2)
    return s


@log
def connect_request(clients):
    w = []
    r = []

    read_clients = []
    write_clients = []

    try:
        r, w, e = select.select(clients, clients, [], 0)
    except Exception as e:
        pass  # Ничего не делать, если какой-то клиент отключился

    if r:
        # Проверяет всех из которых слушает
        for s_client_read in r:
            try:
                read_clients.append(s_client_read)
            except:
                read_clients.remove(s_client_read)
    if w:
        # Проверяет всех кто ждёт сообщения
        for s_client_write in w:
            try:
                write_clients.append(s_client_write)
            except:
                # Удаляем клиента, который отключился
                write_clients.remove(s_client_write)

    return read_clients, write_clients


@log
def client_set(read_clients, write_clients):
    for r_client in read_clients:
        # Рассылает response всем подключившимся и отправившим presence
        presence_message = get_presence(r_client)
        print('Получено от клиента {}'.format(presence_message))
        response = presence_parse(presence_message)
        send_response(response, r_client)
    # Фиаско
    # for w_client in write_clients:
    #     w_client.send('1111'.encode('UTF-8'))


@log
def mainloop():
    address = ('', 7777)
    clients = []
    sock = new_listen_socket(address)

    while True:
        try:
            conn, addr = sock.accept()  # Принимает подключение
        except OSError as e:
            SERVER_LOG.critical('Порт {} занят'.format('7777'), exc_info=True)
            pass                     # timeout вышел
        else:
            print("Получен запрос на соединение с %s" % str(addr))
            clients.append(conn)
        finally:
            # Попытка разделить читающих и пишущих, видимо совсем не так должно это быть
            read_clients, write_clients = connect_request(clients)
            # А потом что-то с ними делать
            client_set(read_clients, write_clients)


print('Сервер запущен')

if __name__ == '__main__':
    mainloop()
