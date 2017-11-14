from socket import socket, AF_INET, SOCK_STREAM
import select

from e_temeplate_func.MyMessage import MyMessMessage
from d_jim.my_jim import MyJimActions, MyJimOtherValue, MyJimField, MyJimResponseCode
from b_server.db.server_db_model import Base
from b_server.db.server_db_def import ServerDbControl


class MyMessServer:
    def __init__(self, name, addr, port):
        self.name = name
        self.addr = addr
        self.port = port
        # запуск сервера
        self.socket = self._start()
        # Все кто будут подключаться
        self._clients = []
        self.db = ServerDbControl('{}.db'.format(self.name), 'b_server/db', Base)

        # Тут все константы для JIM
        self.actions = MyJimActions()
        self.fields = MyJimField()
        self.codes = MyJimResponseCode()
        self.jim_other = MyJimOtherValue()

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
            presence = MyMessMessage()
            presence = presence.mess_get(client_socket)
            print(presence)

            # Спорная проверка
            # TODO: перенести всё в класс MyMessMessage, проверять возможные данные приходящие в action
            if presence['action'] == self.actions.PRESENCE:
                # TODO: получить имя пользователя, добавить в джим ACCOUNT_NAME + слать его с сервера
                # Пока так
                print("Подключается юзер %s" % str(addr))
                # TODO: проверить наличие пользователя в базе, если нет, то добавить 'if not'
                # TODO: запись в историю подключения клиента

                # Оправляет респонс
                response = MyMessMessage(response=self.codes.OK)
                response.response_send(client_socket)
            # TODO: else: - отправлять сообщение о неверном запросе
        except OSError as e:
            pass  # timeout вышел
        else:
            print("Получен запрос на соединение от %s" % str(addr))
            # Добавляем в список подключившегося
            self._clients.append(client_socket)
        finally:
            # Поверяем события
            wait = 0
            r = []
            w = []
            try:
                r, w, e = select.select(self._clients, self._clients, [], wait)
            except:
                pass

            requests = self._read_requests(r)  # Получаем входящие сообщения
            self._write_responses(requests, w)  # Выполним отправку исходящих сообщений

    # Чтение клинтов
    def _read_requests(self, r_clients):
        messages = []

        for sock in r_clients:
            try:
                # Получаем входящие сообщения через метод сервера и лепим в сообщения
                get_message = MyMessMessage().mess_get(sock)
                # УБИРАЕТ ЧЁРТОВО ВРЕМЯ, НЕДЕЛЯ ПОИСКОВ ОШИБКИ РАДИ ЭТОГО КОСТЫЛЯ (
                get_message.pop('time')
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
                if message['action'] == self.jim_other.GET_CONTACTS:
                    client_login = message['user']
                    contacts = self.db.get_contacts(client_login)
                    response = MyMessMessage(response=self.codes.ACCEPTED, quantity=len(contacts))
                    response.response_send(sock)
                    for contact in contacts:
                        contacts_list_send = MyMessMessage(action=self.actions.MSG, message=contact)
                        contacts_list_send.other_send(sock)
                elif message['action'] == self.jim_other.ADD_CONTACT:
                    client_login = message['user']
                    new_contact = message['contact_name']
                    add = self.db.add_contact(client_login, new_contact)
                    if add is not False:
                        self.db.commit()
                        response = MyMessMessage(response=self.codes.ACCEPTED)
                        response.response_send(sock)
                    else:
                        response = MyMessMessage(response=self.codes.WRONG_REQUEST)
                        response.response_send(sock)
                        print('Такой контакт не зарегистрирован')
                    # contacts = self.db.get_contacts(client_login)
                    # response = MyMessMessage(response=self.codes.ACCEPTED, quantity=len(contacts))
                    # response.response_send(sock)
                    # for contact in contacts:
                    #     contacts_list_send = MyMessMessage(action=self.actions.MSG, message=contact)
                    #     contacts_list_send.other_send(sock)
                # else:
                #     try:
                #         transfer = MyMessMessage(**message)
                #         transfer.mess_send(sock)
                #     except:
                #         print('Отключился в записи')
                #         print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
                #         sock.close()
                #         # Чистим общий список клиентов от отвалившихся
                #         self._clients.remove(sock)

    def _get_contacts(self, login):
        contacts = self.db.get_contacts(login)
        return contacts

