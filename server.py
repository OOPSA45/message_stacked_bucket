from socket import *
import time
import json
import logging


# Получает сообщение от клиента
def get_presence(client):
    bpresence = client.recv(1024)
    jpresence = bpresence.decode('utf-8')
    presence = json.loads(jpresence)
    return presence


# Отправляет сообщение клиенту
def send_response(response, client):
    jresponse = json.dumps(response)
    bresponse = jresponse.encode('utf-8')
    client.send(bresponse)


# Форматирует в JIM
def response_format(response_code, time, alert,):
    response = {
        "response": response_code,
        "time": time,
        "alert": alert
    }
    return response


# Формирует ответ клиенту
def presence_parse(presence_message):
    if presence_message['action'] == 'presence':
        response_message = response_format('200', time.time(), 'Presence well done! :: ' + time.ctime(presence_message['time']))
    else:
        response_message = response_format('400', time.time(), 'Unknown query :: ' + time.ctime(presence_message['time']))
    return response_message


if __name__ == '__main__':
    print('Сервер запущен')
    s = socket(AF_INET, SOCK_STREAM)    # Создал сокет TCP
    s.bind(('', 7777))                  # Закрепил адрес
    s.listen(5)                         # Ждёт входящий

    while True:
        client, addr = s.accept()       # Принимает запрос на соединение
        presence_message = get_presence(client)
        print('Получено от клиента {}'.format(presence_message))
        response = presence_parse(presence_message)
        send_response(response, client)
        client.close()


# Основное задание:
# ● Реализовать логгирование с использованием модуля logging:
    # ○ Реализовать декоратор @log, фиксирующий обращение к декорируемой функции:
    # сохраняет имя функции и её аргументы.
    # ○ Настройку логгера выполнить в отдельном модуле log_config.py:
        # ● Создание именованного логгера.
        # ● Сообщения лога должны иметь следующий формат:
        # "<дата-время> <уровень_важности> <имя_модуля> <имя_функции> <сообщение>"
        # ● Журналирование должно производиться в лог-файл.
        # ● На стороне сервера необходимо настроить ежедневную ротацию лог-файлов
        # ● Реализовать обработку нескольких клиентов на сервере с использованием
        # функции select таким образом, что клиенты общаются в "общем чате", т.е.
        # каждое сообщение каждого клиента отправляется всем клиентам,
        # подключенным к серверу.
        # ● Реализовать функции отправки/приёма данных на стороне клиента. Для
        # упрощения разработки приложения на данном этапе пусть клиентское
        # приложение будет либо только принимать, либо только отправлять сообщения в
        # общий чат:
        # ● запуск скрипта клиента должен осуществляться с параметром командной
        # строки: -r (чтение чата) или -w (передача сообщений в чат).
        # ● Для всех функций необходимо написать тесты.