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


# Отправляем JSON на сервер
def send_to_server(json_massege):
    s.send(json_massege.encode('utf-8'))


# Форматируем ответ для вывода в клиенте
def message_format(server_answer):
    view_message = 'Получен код: ' + server_answer['response'] + "\n"
    view_message += 'Сообщение от сервера: ' + server_answer['alert'] + "\n"
    print(view_message)
    if server_answer['response'] == '200':
        server_chat()


def server_chat():
    keyboard = input('Введите сообщение: ')
    if keyboard != 'quit':
        mess = format_action('msg', keyboard)
        send_to_server(mess)
    else:
        mess = format_action('quit')
        send_to_server(mess)
        return s.close()
    server_answer = json.loads(s.recv(1024))    # Принимаем ответ сервера и распарсиваем JSON
    message_format(server_answer)

message = format_action('presence')         # Формируем presence сообщение
send_to_server(message)                     # Отправляем сообщение на сервер
server_answer = json.loads(s.recv(1024))    # Принимаем ответ сервера и распарсиваем JSON
message_format(server_answer)