"""
    ● сформировать presence-сообщение;
    ● отправить сообщение серверу;
    ● получить ответ сервера;
    ● разобрать сообщение сервера;
    ● параметры командной строки скрипта client.py <addr> [<port>]:
        ○ addr - ip-адрес сервера;
        ○ port - tcp-порт на сервере, по умолчанию 7777.
"""


from socket import *
import time
import json

s = socket(AF_INET, SOCK_STREAM)    # Создал сокет TCP

# ○ addr - ip-адрес сервера;
# ○ port - tcp-порт на сервере, по умолчанию 7777.
s.connect(('localhost', 7777))      # Соединился с сервером


# ● сформировать presence-сообщение в JIM def;
def presence_format(action, time):
    message = {
        'action': action,
        'time': time,
    }
    return json.dumps(message)


# ● разобрать сообщение сервера def;
def response_parse(response):
    output = 'Response code: ' + response['response'] + "\n"
    output += '--- ' + response['alert'] + ' ---'
    return output


presence = presence_format('presence', time.time())     # ● сформировать presence-сообщение var;
s.send(presence.encode('utf-8'))                        # ● отправить сообщение серверу + кодировки;

response = json.loads(s.recv(1024))         # ● получить ответ сервера + JSON parse;
print(response_parse(response))             # ● разобрать сообщение сервера var + print();
s.close()