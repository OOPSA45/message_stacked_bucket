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
        # Все кто будут подключаться, собирает сокеты в список
        self._clients = []
        # Создаёт db
        self.db = ServerDbControl('{}.db'.format(self.name), 'b_server/db', Base)

        # Собирает имена подключившихся клиентов {'имя': 'сокет'}
        self.client_names = {}
        self.client_name = 'Guest'

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
        from_client_name = self.client_name
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
                # Получаем имя подключившегося юзера
                from_client_name = presence['user'][self.jim_other.ACCOUNT_NAME]
                # Пока так
                print("Подключается юзер ---{}--- адрес: {}".format(from_client_name, str(addr)))
                # TODO: проверить наличие пользователя в базе, если нет, то добавить 'if not'
                # TODO: запись в историю подключения клиента

                # Оправляет респонс
                response = MyMessMessage(response=self.codes.OK)
                response.response_send(client_socket)
            # TODO: else: - отправлять сообщение о неверном запросе
        except OSError as e:
            pass  # timeout вышел
        else:
            print("Юзер ---{}--- успешно подключился".format(from_client_name))
            # Добавляем в список подключившегося
            self._clients.append(client_socket)
            # Добавляем имя клиента в словарь - имя: сокет
            self.client_names[from_client_name] = client_socket
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
                # Сохраняем сообщение + сокет от которого оно пришло
                messages.append((get_message, sock))
            except:
                print('Отключился в чтении')
                print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
                # Чистим общий список клиентов от отвалившихся
                self._clients.remove(sock)

        # Возвращаем словарь сообщений
        return messages

    def _write_responses(self, messages, w_clients):
        for client_said in messages:
            # from_name = соккет от которого пришло сообщение. Пока ни где не используется
            message, from_name = client_said

            to_client = None
            sock = None

            # Будем проверять, указан ли получатель
            if 'to' in message['user']:
                # Если указанно имя получателя
                if message['user']['to'] is not None:
                    # Находим имя
                    to_client = message['user']['to']
            else:
                # Иначе считаем, что отправитель сам же является получателем
                to_client = message['user']
                # Находим сокет по имени
            if to_client is not None:
                sock = self.client_names[to_client]

            if message['action'] == self.jim_other.GET_CONTACTS:
                print('Клиент запросил контакты')
                client_login = message['user']
                contacts = self.db.get_contacts(client_login)
                response = MyMessMessage(response=self.codes.ACCEPTED, quantity=len(contacts))
                print('Список контактов клиента {}'.format(contacts))
                response.response_send(sock)
                # Перебираем и отправляем контакты
                for contact in contacts:
                    contacts_list_send = MyMessMessage(action=self.actions.MSG, message=contact)
                    print('Нужно что-то распечатать, '
                          'иначе он запихнёт первые 2 контакта в одну строку. '
                          'Хз как это побороть')
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
            elif message['action'] == self.actions.MSG:
                # Если есть имя клиента которому отправляем
                # TODO: проверять в БД существует такой клиент или нет
                # TODO: а потом проверять есть ли связь между клиентами from и to
                if sock is not None:
                    # Формируем сообщение и пуляем на сокет соответствующий имени
                    transfer = MyMessMessage(**message)
                    transfer.mess_send(sock)
                else:
                    # Если нет, то отправлять будем всем кто читает!
                    for sock in w_clients:
                        transfer = MyMessMessage(**message)
                        transfer.mess_send(sock)
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

