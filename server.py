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


if __name__ == '__main__':
    print('Сервер запущен')
    s = socket(AF_INET, SOCK_STREAM)    # Создал сокет TCP
    port = 7777
    try:
        s.bind(('', port))  # Закрепил адрес
    except OSError:
        # Пишет ошибку в лог
        SERVER_LOG.critical('Порт {} занят'.format(port), exc_info=True)
        # sys.exc_info()[1],

    s.listen(5)                         # Ждёт входящий

    while True:
        client, addr = s.accept()       # Принимает запрос на соединение
        presence_message = get_presence(client)
        print('Получено от клиента {}'.format(presence_message))
        response = presence_parse(presence_message)
        send_response(response, client)
        client.close()