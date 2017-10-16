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


class MyMessMessage:
    def __init__(self, cur_socket, raw_message=None):
        self.cur_socket = cur_socket
        self.raw_message = raw_message

    def mess_send(self):
        self.cur_socket.send(self.mess_format().encode('utf-8'))
        return self.mess_format().encode('utf-8')

    @property
    def mess_get(self):
        mess = json.loads(self.cur_socket.recv(1024).decode('utf-8'))
        return mess

    def mess_format(self):
        self.raw_message['time'] = time.time()
        json_message = json.dumps(self.raw_message)
        return json_message


class MyMessClient:
    def __init__(self):
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.presence = MyMessMessage(self.client_socket, {'action': 'presence'})

    def client_connect(self):
        try:
            self.client_socket.connect(('localhost', 7777))
        except ConnectionRefusedError:
            print('Ошибка подключения')
        else:
            self.presence.mess_send()
        finally:
            response = MyMessMessage(self.client_socket)
            print(response.mess_get)


class MyMessServer:
    def __init__(self):
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.bind(('', 7777))
        self.server_socket.listen(5)
        print('Сервер запущен')

    def server_accept_in(self):
        client_socket, addr = self.server_socket.accept()
        self.get_client_query(client_socket)

    def get_client_query(self, client_socket):
        get_message = MyMessMessage(client_socket).mess_get
        self.server_mess_identify(get_message, client_socket)
        return get_message

    def server_mess_identify(self, mess, client_socket):
        if mess['action'] == 'presence':
            print('Получено от клиента {}'.format(mess))
            self.server_send_response(client_socket)

    def server_send_response(self, client_socket):
        response = MyMessMessage(client_socket, {'response': '200', 'alert': 'Well done!'})
        response.mess_send()

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

#
# class MyMessStorage:
#     def __init__(self):
#     pass