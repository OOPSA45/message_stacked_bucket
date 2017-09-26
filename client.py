from socket import *
import time
import json

s = socket(AF_INET, SOCK_STREAM)  # Создать сокет TCP
s.connect(('localhost', 8888))   # Соединиться с сервером

# Преобразуем соосбещние в JIM и конвертим в JSON
def format_action(action, text = None):
    message = {
        'action': action,
        'time': time.time(),
    }

    if text is not None:
        message.update({'message': text})

    on_output = json.dumps(message)
    return on_output


# Форматируем ответ для вывода в клиенте
def message_format(server_answer):
    view_message = 'Response code: ' + server_answer['response'] + "\n"
    view_message += '--- ' + server_answer['alert'] + " ---\n"
    print(view_message)

message = format_action('presence')         # Формируем presence сообщение
s.send(message.encode('utf-8'))                  # Отправляем сообщение на сервер
server_answer = json.loads(s.recv(1024))    # Принимаем ответ сервера и распарсиваем JSON
message_format(server_answer)