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
def format_response(response_code, alert):
    response_jim = {
        "response": response_code,
        "time": time.time(),
        "alert": alert
    }
    return json.dumps(response_jim)


# ● формирует ответ клиенту def;
def response_format(presence):
    if presence['action'] == 'presence':
        response = format_response('200', 'Presence well done! ' + time.ctime(presence['time']))
    # elif data['action'] == 'msg':
    #     answer = format_response('200', time.ctime(data['time']))
    else:
        response = format_response('100', 'Unknown query --- ' + time.ctime(presence['time']))
    return response


while True:
    result = s.accept()                         # Принял запрос на соединение
    client, addr = result
    presence = json.loads(client.recv(1024))    # ● принимает сообщение клиента + JSON parse;
    response = response_format(presence)        # ● формирует ответ клиенту var;
    client.send(response.encode('utf-8'))       # ● отправляет ответ клиенту;
    client.close()
