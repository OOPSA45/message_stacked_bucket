from socket import socket, AF_INET, SOCK_STREAM
import select

from temeplate_func.MyMessage import MyMessMessage
from jim.my_jim import MyJimActions

from server.schema.schema import DbAction


class MyMessServer:
    def __init__(self, addr, port):
        self.addr = addr
        self.port = port
        # запуск сервера
        self.socket = self._start()
        self.action = MyJimActions()
        # Все кто будут подключаться
        self._clients = []
        self.repo = DbAction('server.db')

    def _start(self):
        s = socket(AF_INET, SOCK_STREAM)
        s.bind((self.addr, self.port))
        s.listen(5)
        # Задержка обработки событий
        s.settimeout(0.2)
        return s

    def main_loop(self):
        while True:
            self._get_accept_in()

    # Принимает подключения (всё как в примере)
    def _get_accept_in(self):
        try:
            # Принимает коннект от клиента
            client_socket, addr = self.socket.accept()
            # Ловит пресенс от клиента
            presence = MyMessMessage(client_socket)
            presence = presence.mess_get
            print(presence)

            # Спорная проверка
            # TODO: перенести всё в класс MyMessMessage, проверять возможные данные приходящие в action
            if presence['action'] == self.action.PRESENCE:
                # TODO: получить имя пользователя, добавить в джим ACCOUNT_NAME + слать его с сервера
                # Пока так
                print("Подключается юзер %s" % str(addr))
                # TODO: проверить наличие пользователя в базе, если нет, то добавить 'if not'
                # TODO: запись в историю подключения клиента

                # Оправляет респонс
                response = MyMessMessage(client_socket, {'response': '200', 'alert': 'Well done!'})
                response.response_send()
            # TODO: else: - отправлять сообщение о неверном запросе
        except OSError as e:
            pass  # timeout вышел
        else:
            print("Получен запрос на соединение от %s" % str(addr))
            # Добавляем в список подключившегося
            self._clients.append(client_socket)
            # print(self._clients)
        finally:
            # Поверяем события
            wait = 0
            r = []
            w = []
            try:
                r, w, e = select.select(self._clients, self._clients, [], wait)
            except:
                pass

            # print(r)
            requests = self._read_requests(r)  # Получаем входящие сообщения
            self._write_responses(requests, w)  # Выполним отправку исходящих сообщений

    # Чтение клинтов
    def _read_requests(self, r_clients):
        messages = []

        for sock in r_clients:
            try:
                # Получаем входящие сообщения через метод сервера и лепим в сообщения
                get_message = MyMessMessage(sock).mess_get
                print('Получено от клиента {}'.format(get_message))
                messages.append(get_message)
            except:
                print('Отключился в чтении')
                print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
                # Чистим общий список клиентов от отвалившихся
                self._clients.remove(sock)

        # Возвращаем словарь сообщений
        return messages

    def _write_responses(self, messages, w_clients):
        for sock in w_clients:
            for message in messages:
                try:
                    # TODO: работает с косяком, ошибка где-то в классе протокола
                    transfer = MyMessMessage(sock, {'action': 'msg', 'message': message})
                    transfer.mess_send()
                except:
                    print('Отключился в записи')
                    print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
                    sock.close()
                    # Чистим общий список клиентов от отвалившихся
                    self._clients.remove(sock)
