from socket import *
import json
import time
import select

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
        # Сначала форматирует в JSON
        self.cur_socket.send(self.mess_format().encode('utf-8'))
        return self.mess_format().encode('utf-8')

    # Умеет получать сообщения
    @property
    def mess_get(self):
        # Получает и сразу декодирует
        mess = json.loads(self.cur_socket.recv(1024).decode('utf-8'))
        return mess

    # Форматирование + время для JIM
    def mess_format(self):
        self.raw_message['time'] = time.time()
        json_message = json.dumps(self.raw_message)
        return json_message

# Класс клиент
class MyMessClient:
    def __init__(self):
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.presence = MyMessMessage(self.client_socket, {'action': 'presence'})

    # Подключается
    def client_connect(self):
        try:
            self.client_socket.connect(('localhost', 7777))
        except ConnectionRefusedError:
            print('Ошибка подключения')
        else:
            # Если всё ок, то отправляет пресенс
            self.presence.mess_send()
        finally:
            # Ждёт респонса
            response = MyMessMessage(self.client_socket)
            print(response.mess_get)
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