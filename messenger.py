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
import select


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
            mode = input('r/w?: ')
            self.client_chat(mode)

    def client_chat(self, mode):

        if mode == 'r':
            # читаем сообщения и выводим на экран
            while True:
                new_message = MyMessMessage(self.client_socket)
                print(new_message.mess_get)
        elif mode == 'w':
            # ждем ввода сообщения и шлем на сервер
            while True:
                message = input(':) >')
                self.client_socket.send(json.dumps({'action': 'msg', 'message': message}).encode('UTF-8'))
                # new_message = MyMessMessage(self.client_socket, {'action': 'msg', 'message': message})
                # new_message.mess_send()


class MyMessServer:
    def __init__(self):
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.bind(('', 7777))
        self.server_socket.listen(5)
        print('Сервер запущен')

    def server_accept_in(self):
        clients = []
        while True:
            try:
                client_socket, addr = self.server_socket.accept()
            except OSError as e:
                pass
            else:
                print("Получен запрос на соединение от %s" % str(addr))
                clients.append(client_socket)
            finally:
                wait = 0
                r = []
                w = []
                try:
                    r, w, e = select.select(clients, clients, [], wait)
                except:
                    pass  # Ничего не делать, если какой-то клиент отключился

                requests = self.read_requests(r, clients)
                self.write_responses(requests, w, clients)  # Выполним отправку входящих сообщений

    def read_requests(self, r_clients, all_clients):
        messages = []
        for sock in r_clients:
            try:
                # Получаем входящие сообщения
                messages.append(self.get_client_query(sock))
            except:
                print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
                all_clients.remove(sock)

        # Возвращаем словарь сообщений
        return messages

    def write_responses(self, messages, w_clients, all_clients):
        for sock in w_clients:
            # Будем отправлять каждое сообщение всем
            for message in messages:
                try:
                    # Подготовить и отправить ответ сервера
                    self.server_send_response(sock, message)
                except:  # Сокет недоступен, клиент отключился
                    print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
                    sock.close()
                    all_clients.remove(sock)

    def get_client_query(self, client_socket):
        get_message = MyMessMessage(client_socket).mess_get
        self.server_mess_identify(get_message, client_socket)
        return get_message

    def server_mess_identify(self, mess, client_socket):
        if mess['action'] == 'presence':
            print('Получено от клиента {}'.format(mess))
            self.server_send_response(client_socket)
        elif mess['action'] == 'msg':
            print('Получено от клиента {}'.format(mess))

    def server_send_response(self, client_socket, mess='Well done!'):
        response = MyMessMessage(client_socket, {'response': '200', 'alert': mess})
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