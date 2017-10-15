# 1.	Класс JIMСообщение - класс, реализующий сообщение (msg) по протоколу JIM.
# 2.	Класс JIMОтвет - класс, реализующий ответ (response) по протоколу JIM.

# 3.	Класс Клиент - класс, реализующий клиентскую часть системы.

# 4.	Класс Чат - класс, обеспечивающий взаимодействие двух клиентов.

# 5.	Класс ЧатКонтроллер - класс, обеспечивающий передачу данных из Чата в ГрафическийЧат и обратно; обрабатывает события от пользователя (ввод данных, отправка сообщения).

# 6.	Класс ГрафическийЧат - базовый класс, реализующий интерфейс пользователя (UI) - вывод сообщений чата, ввод данных от пользователя - служит базой для разных интерфейсов пользователя (консольный, графический, WEB).
#           ■	Дочерний класс КонсольныйЧат - обеспечивает ввод/вывод в простой консоли.
# 7.	Класс Сервер - базовый класс сервера мессенджера; может иметь разных потомков - работающих с потоками или выполняющих асинхронную обработку.
# 8.	Класс Хранилище - базовый класс, обеспечивающий сохранение данных (сохранение информации о пользователях на сервере, сохранение сообщений на стороне клиента).
#           ■	Дочерний класс ФайловоеХранилище - обеспечивает сохранение информации в текстовых файлах

from socket import *
import json
import time


# MyMessMessage({'type': 'action', 'code': 'presence'}, time.time(), {'type': 'alert', 'message': 'test'})
class MyMessMessage:
    def __init__(self, cur_socket, action, cur_time, alert=None):
        self.cur_socket = cur_socket
        self.action_type = action['type']
        self.action_code = action['code']
        self.time = time.ctime(cur_time)
        self.alert = alert

        if self.alert is not None:
            self.alert_type = alert['type']
            self.alert_mess = alert['message']

    def mess_format(self):
        json_message = {
            self.action_type: self.action_code,
            'time': self.time,
        }
        if self.alert is not None:
            json_message[self.alert_type] = self.alert_mess

        json_message = json.dumps(json_message)
        return json_message

    def mess_send(self):
        self.cur_socket.send(self.mess_format().encode('utf-8'))
        return self.mess_format().encode('utf-8')


class MyMessResponse:
    def __init__(self, cur_socket):
        self.cur_socket = cur_socket

    @property
    def resp_decode(self):
        response = json.loads(self.cur_socket.recv(1024).decode('utf-8'))
        return '{} {} {}'.format(response['response'], response['alert'], response['time'])


class MyMessClient:
    def __init__(self):
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.presence = MyMessMessage(self.client_socket, {'type': 'action', 'code': 'presence'}, time.time())

    def client_connect(self):
        try:
            self.client_socket.connect(('localhost', 7777))
        except ConnectionRefusedError:
            print('Ошибка подключения')
        else:
            self.presence.mess_send()
        finally:
            response = MyMessResponse(self.client_socket)
            print(response.resp_decode)


client = MyMessClient()
client.client_connect()


# class MyMessChat:
#     def __init__(self):
#     pass
#
# class MyMessChatC:
#     def __init__(self):
#     pass
#
# class MyMessGraphicChat:
#     def __init__(self):
#     pass
#
# class MyMessServer:
#     def __init__(self):
#     pass
#
# class MyMessStorage:
#     def __init__(self):
#     pass