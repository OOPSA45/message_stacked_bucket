from socket import socket, AF_INET, SOCK_STREAM
import threading
from queue import Queue

from e_temeplate_func.MyMessage import MyMessMessage
from a_client.db.client_db_def import ClientDbControl
from a_client.db.client_db_model import Base

from b_server.db.server_db_def import ServerDbControl
from d_jim.my_jim_conf import MyJimOtherValue, MyJimActions, MyJimResponseCode, MyJimField


class MyMessReceiver:
    # Получает сокет, получает очередь
    def __init__(self, sock, sock_in_queue):
        self.sock = sock
        self.sock_in_queue = sock_in_queue

        self.jim_other = MyJimOtherValue()
        self.actions = MyJimActions()
        self.codes = MyJimResponseCode()
        self.fields = MyJimField()

    def __call__(self):
        self.is_alive = True
        while True:
            if not self.is_alive:
                break
            # Принимает сообщение по протоколу
            # data = MyMessMessage()
            # d = data.mess_get(self.sock)

            # Получает респонс
            listen_sct = MyMessMessage()
            response = listen_sct.mess_get(self.sock)
            # print('Поток в ресивере {}'.format(response))
            # TODO: тут должны быть очереди
            if self.fields.RESPONSE in response:
                if response[self.fields.RESPONSE] == self.codes.OK:
                    print('Грит {} ---- Полный {}'.format(response['response'], response))
                elif response[self.fields.RESPONSE] == self.codes.ACCEPTED:
                    print('Запрос успешен {}'.format(response))
                else:
                    print('Неверный код ответа от сервера')
            elif self.fields.ACTION in response:
                if response[self.fields.ACTION] == self.actions.MSG:
                    print('{} говорит --> {}'.format(
                        response[self.jim_other.USER][self.jim_other.FROM],
                        response[self.fields.MESSAGE])
                    )
                elif response[self.fields.ACTION] == self.actions.RESPONSE:
                    print('Контакт << {} >> получен'.format(response[self.fields.MESSAGE]))

            # TODO: принты и очередь


class MyMessClient:
    def __init__(self, name, addr='localhost', port=7777):
        self.name = name
        self.addr = addr
        self.port = port
        # Подключиться
        self.socket = self._connect()

        # Создаём базу для клиента
        self.db = ClientDbControl('{}.db'.format(self.name), 'a_client/db', Base)
        # TODO: так быть не должно, всё это нужно делать на сервере
        # Сразу пишем туда подключившегося юзера
        self.add_to_client_db()
        # TODO: так быть не должно, всё это нужно делать на сервере
        '''
        Костыли [start]
        '''
        # Подключаемся к базе сервера и пишем туда клиента и хистори
        self.server_db = ServerDbControl('server.db', 'b_server/db', Base)
        self.add_toserver_db()
        '''
        Костыли [end]
        '''

        self.jim_other = MyJimOtherValue()
        self.actions = MyJimActions()
        self.codes = MyJimResponseCode()

        # Пресенс по дефолту
        self.presence = MyMessMessage(action=self.actions.PRESENCE, user={self.jim_other.ACCOUNT_NAME: self.name})

        # тут будет очередь
        self.request_queue = Queue()

        # Стартует GUI - пока не стартуем, только экземпяр хз для чего, но мб пригодится
        # self.gui = MyGui()
        '''
        self._gui_start() запустится после получения списка контактов - не запустится
        '''

    def _connect(self):
        # Создать сокет TCP
        sct = socket(AF_INET, SOCK_STREAM)
        # Соединиться с сервером
        sct.connect((self.addr, self.port))
        return sct

    def disconnect(self):
        # Отключаемся
        self.socket.close()

    # Костыли. Использовалось для вывода контактов в GUI на прямую после старта клинта. GUI пока отключено
    # работает только для записи новых клиентов в базу
    '''
    Костыли [start]
    '''
    def add_to_client_db(self):
        self.db.add_user(self.name)
        self.db.commit()

    def add_toserver_db(self):
        self.server_db.add_client(self.name)
        self.server_db.add_history(self.name, self.addr)
        self.server_db.commit()
    '''
    Костыли [/end]
    '''

    # Метод для старта GUI, но заработает видимо только после подключения потоков :(
    # def gui_start(self, contact_list):
        # Запрос на контакты на прямую у сервера
        # TODO: перенести всё это на сервер и запрашивать через JIM. А JIM работает косячно.
        # contacts = self.server_db.get_contacts(self.name)
        # self.gui.view_contact(contact_list)
        # self.gui.start_gui()

    def client_start(self):
        # Отправляет пресенс
        self.presence.mess_send(self.socket)

        # Эм, ресивер. Будет слушать
        listener = MyMessReceiver(self.socket, self.request_queue)
        th_listen = threading.Thread(target=listener)
        th_listen.daemon = True
        th_listen.start()
        # TODO: расшифровка респонса и нормальный вывод
        while True:
            to_user_name = None
            message_str = input('...> ')
            if message_str.startswith('list'):
                self.get_contacts()
            elif message_str.startswith('add'):
                try:
                    new_name = message_str.split()[1]
                except IndexError:
                    print('Нет имени')
                else:
                    self.add_contact(new_name)
            else:
                '''
                Если это будет просто сообщение
                то будем искать в нём имя клиента, пока так - ...> message <name to>
                '''
                try:
                    # И если второй параметр существует, то забираем его в качестве имени
                    to_user_name = message_str.split()[1]
                except IndexError:
                    # Если нет, то имя будет None, и тогда сервер разошлёт это сообщение всем читающим
                    pass
                # Создаем сообщение по протоколу
                msg = MyMessMessage(action=self.actions.MSG, message=message_str, user={
                    self.jim_other.FROM: self.name,
                    self.jim_other.TO: to_user_name
                })
                # Отправляем на сервер
                msg.mess_send(self.socket)

    # Чтобы получать контакты
    def get_contacts(self):
        """Получить список контактов"""
        # формируем сообщение
        list_message = MyMessMessage(action=self.jim_other.GET_CONTACTS, user=self.name)
        # отправляем
        list_message.other_send(self.socket)

    def add_contact(self, new_name):
        add_contact = MyMessMessage(action=self.jim_other.ADD_CONTACT, user=self.name, contact_name=new_name)
        add_contact.other_send(self.socket)
