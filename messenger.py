from socket import socket, AF_INET, SOCK_STREAM
import json
import time
import select

# База, иснталит все нужные таблицы
import schema.my_schema

# JIM протокол
from jim.my_jim import MyJimMessage, MyJimResponse

# TODO подключить логер log.log_config, сам класс где-то в репозитории валяется
# TODO тесты .py, когда не известно

# Почти работает, но это не точно


# Класс сообщение
class MyMessMessage:
    def __init__(self, cur_socket, raw_message=None):
        # Сокет
        self.cur_socket = cur_socket
        # Не форматированное сообщение
        self.raw_message = raw_message

    # Умеет отправлять сообщения
    def mess_send(self):
        # Отправляем в класс JIM
        message = MyJimMessage(**self.raw_message, time=time.time())
        self.cur_socket.send(bytes(message))
        return message

    # Умеет отправлять респонсы
    def response_send(self):
        # Отправляем в класс JIM
        message = MyJimResponse(**self.raw_message, time='Time to kill!')
        self.cur_socket.send(bytes(message))
        return message

    # Умеет получать сообщения
    @property
    def mess_get(self):
        # Получает и сразу декодирует
        mess = json.loads(self.cur_socket.recv(1024).decode('utf-8'))
        return mess

    def __str__(self):
        return self.raw_message


# Класс клиент
class MyMessClient:
    def __init__(self):
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.presence = MyMessMessage(self.client_socket, {'action': 'presence'})
        self.client_socket.connect(('localhost', 7777))

    # Подключается
    def client_connect(self):
            # Отправляет пресенс
            # TODO: надо бы проверки сделать
            self.presence.mess_send()
            # Ждёт респонса
            serv_response = MyMessMessage(self.client_socket)
            response = serv_response.mess_get
            print(response)
            # Дальше ввод с клавы читать/слушать
            mode = input('r/w?: ')
            self.client_chat(mode)

    # Метод режима работы клиента
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


# Класс сервер
class MyMessServer:
    def __init__(self):
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.bind(('', 7777))
        self.server_socket.listen(5)
        print('Сервер запущен')

    # Принимает подключения (всё как в примере)
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
                    pass

                requests = self.read_requests(r, clients)
                self.write_responses(requests, w, clients)

    def read_requests(self, r_clients, all_clients):
        messages = []
        for sock in r_clients:
            try:
                # Получаем входящие сообщения через метод сервера
                messages.append(self.get_client_query(sock))
            except:
                print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
                all_clients.remove(sock)

        # Возвращаем словарь сообщений
        return messages

    def write_responses(self, messages, w_clients, all_clients):
        for sock in w_clients:
            # Будем отправлять каждое сообщение всем
            # mess = json.dumps({'response': '200', 'alert': 'Well done!'}).encode('UTF-8')
            # sock.send(mess)
            # print(sock)
            for message in messages:
                try:
                    # Подготовить и отправить ответ сервера через метод
                    self.server_send_response(sock, message)
                except:
                    print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
                    sock.close()
                    all_clients.remove(sock)

    # Получает клиентские сообщения
    def get_client_query(self, client_socket):
        get_message = MyMessMessage(client_socket).mess_get
        self.server_mess_identify(get_message, client_socket)
        return get_message

    # Определяет тип клиентского сообщения
    def server_mess_identify(self, mess, client_socket):
        if mess['action'] == 'presence':
            print('Получено от клиента {}'.format(mess))
            # Если был пресенс - то отправляет респонс 200 в ответ
            self.server_send_response(client_socket)
        elif mess['action'] == 'msg':
            print('Получено от клиента {}'.format(mess))

    # Метод ответа (не дописал)
    def server_send_response(self, client_socket):
        response = MyMessMessage(client_socket, {'response': '200', 'alert': 'Well done!'})
        response.response_send()

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