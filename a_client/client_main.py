from socket import socket, AF_INET, SOCK_STREAM

from e_temeplate_func.MyMessage import MyMessMessage
from a_client.db.client_db_def import ClientDbControl
from a_client.db.client_db_model import Base

from c_intetrface.start_form import MyGui

from b_server.db.server_db_def import ServerDbControl

from d_jim.my_jim_conf import MyJimOther, MyJimActions


class MyMessClient:

    def __init__(self, name, addr='localhost', port=7777):
        self.name = name
        self.addr = addr
        self.port = port
        # Подключиться
        self.socket = self._connect()

        # Создаём базу для клиента
        self.db = ClientDbControl('{}.db'.format(self.name), 'a_client/db', Base)

        # Сразу пишем туда подключившегося юзера
        self.add_to_client_db()

        # Подключаемся к базе сервера и пишем туда клиента и хистори
        self.server_db = ServerDbControl('server.db', 'b_server/db', Base)
        self.add_toserver_db()

        self.jim = MyJimOther()
        self.actions = MyJimActions()

        # Пресенс по дефолту
        self.presence = MyMessMessage(action=self.actions.PRESENCE)
        # print(self.presence)

        # Стартует GUI
        self.gui = MyGui()
        '''
        self._gui_start() запустится после респонса
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

    def get_contacts(self):
        """Получить список контактов"""
        # формируем сообщение
        list_message = MyMessMessage(action=self.jim.GET_CONTACTS)
        # отправляем
        list_message.other_send(self.socket)
        # Принять не более 1024 байтов данных
        list_message.mess_get(self.socket)
        contact_list = list_message.mess_get(self.socket)
        print(contact_list)
        # message_bytes = self.socket.recv(1024)
        # # Формируем сообщение из байт
        # jm = JimResponse.create_from_bytes(message_bytes)
        # if jm.response == ACCEPTED:
        #     # Ждем второе сообщение со списком контактов
        #     message_bytes = self.socket.recv(1024)
        #     jm = JimMessage.create_from_bytes(message_bytes)
        #     # выводим список контактов
        #     contact_list = jm.action
        #     print(contact_list)
        #     # обновляем наш список контактов, на сервере правильный
        #     self.repo.clear_contacts()
        #     for contact in contact_list:
        #         self.repo.add_contact(contact)
        #     return contact_list
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

    def gui_start(self):
        # Запрос на контакты на прямую у сервера
        # TODO: перенести всё это на сервер и запрашивать через JIM. А JIM работает косячно.
        contacts = self.server_db.get_contacts(self.name)
        self.gui.view_contact(contacts)
        self.gui.start_gui()

    def client_start(self):
        # TODO: надо бы проверки сделать

        # Отправляет пресенс
        self.presence.mess_send(self.socket)

        # TODO: тесты. Без тестов ничерта не понятно что вернётся и как это проверять дальше
        # Получает респонс
        # Может так не очень верно, но создаёт экземпляр с сокетом для начала...
        listen_sct = MyMessMessage()
        # ...далее слушает его. Получает уже очишенные значения от байтов
        response = listen_sct.mess_get(self.socket)

        # TODO: подключить JIM -->
        """
        Как сделать многострочный TODO?
        --> возможно в MyMessMessage() нужно сделать отдельный метод .response_get
        с подключённым MyJimResponse().create_from_bytes
        и использовать вместо .mess_get
        """
        # Но чёт не вижу смысла проверять или гонять его через JIM, на входе же есть всё эт

        # Если есть респонс
        # Не тестировал, но поидее класс должен сразу возвращать сюда ошибку
        if response['response']:
            # TODO: расшифровка респонса и нормальный вывод
            print('Грит {} ---- Полный {}'.format(response['response'], response))

            # self.gui_start()

            mode = input('r/w?')
            if mode == 'r':
                # Читает
                print('Слушаю')
                while True:
                    # Принять не более 1024 байтов данных
                    # message_bytes = self.socket.recv(1024)
                    """
                    Что-то принимаем от сервера
                    """
                    # Мы же выше уже сделали экземпляр с текущим сокетом для респонса, слушаем его же
                    message = listen_sct.mess_get(self.socket)
                    print(message)
            elif mode == 'w':
                # Пишет
                print('Говорю')
                while True:
                    message_str = input('...> ')
                    if message_str.startswith('list'):
                        self.get_contacts()
                    # Создаем сообщение по протоколу
                    # Ох, костыли, но работает же
                    msg = MyMessMessage(action=self.actions.MSG, message=message_str)
                    # Отправляем на сервер
                    msg.mess_send(self.socket)
            else:
                print('Нет такого варианта {}'.format(mode))
        # elif presence_response.response == SERVER_ERROR:
        #     print('Внутрення ошибка сервера')
        # elif presence_response.response == WRONG_REQUEST:
        #     print('Неверный запрос на сервер')

            # Получить контакты текущего юзера
        else:
            print('Неверный код ответа от сервера')
