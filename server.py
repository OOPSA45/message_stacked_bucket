"""
    ● принимает сообщение клиента;
    ● формирует ответ клиенту;
    ● отправляет ответ клиенту;
    ● имеет параметры командной строки:
        ○ -p <port> - TCP-порт для работы (по умолчанию использует порт 7777);
        ○ -a <addr> - IP-адрес для прослушивания (по умолчанию слушает все доступные адреса).
"""


from socket import *
import time
import json

s = socket(AF_INET, SOCK_STREAM)    # Создал сокет TCP

# ○ -a <addr> - IP-адрес для прослушивания (по умолчанию слушает все доступные адреса).
# ○ -p <port> - TCP-порт для работы (по умолчанию использует порт 7777);
s.bind(('', 7777))                  # Закрепил адрес
s.listen(5)                         # Ждёт входящий


# Форматирует ответ в JIM
def response_format(response_code, time, alert,):
    response = {
        "response": response_code,
        "time": time,
        "alert": alert
    }
    return json.dumps(response)


# ● формирует ответ клиенту
def presence_parse(presence):
    if presence['action'] == 'presence':
        response = response_format('200', time.time(), 'Presence well done! :: ' + time.ctime(presence['time']))
    else:
        response = response_format('100', time.time(), 'Unknown query :: ' + time.ctime(presence['time']))
    return response


while True:
    result = s.accept()                         # Принимает запрос на соединение
    client, addr = result
    presence = json.loads(client.recv(1024))    # ● принимает сообщение клиента + JSON parse;
    response = presence_parse(presence)         # ● формирует ответ клиенту
    client.send(response.encode('utf-8'))       # ● отправляет ответ клиенту
    client.close()




