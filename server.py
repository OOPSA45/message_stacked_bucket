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

# Создал сокет и слушаю
s = socket(AF_INET, SOCK_STREAM)    # Создал сокет TCP

# ○ -a <addr> - IP-адрес для прослушивания (по умолчанию слушает все доступные адреса).
# ○ -p <port> - TCP-порт для работы (по умолчанию использует порт 7777);
s.bind(('', 7777))                  # Запрепил адрес
s.listen(5)                         # Жду входящий


# Привожу ответ к клиенту к формату JIM
def response_format(response_code, alert):
    response = {
        "response": response_code,
        "time": time.time(),
        "alert": alert
    }
    return json.dumps(response)


# ● формирует ответ клиенту def;
def presence_parse(presence):
    if presence['action'] == 'presence':
        response = response_format('200', 'Presence well done! :: ' + time.ctime(presence['time']))
    else:
        response = response_format('100', 'Unknown query :: ' + time.ctime(presence['time']))
    return response


while True:
    result = s.accept()                         # Принял запрос на соединение
    client, addr = result
    presence = json.loads(client.recv(1024))    # ● принимает сообщение клиента + JSON parse;
    response = presence_parse(presence)         # ● формирует ответ клиенту var;
    client.send(response.encode('utf-8'))       # ● отправляет ответ клиенту;
    client.close()
