from socket import socket, AF_INET, SOCK_STREAM

from temeplate_func.MyMessage import MyMessMessage
from client.schema.schema import DbAction


class MyMessClient:

    def __init__(self, addr='localhost', port=7777):
        self.addr = addr
        self.port = port
        # Подключиться
        self.socket = self._connect()
        # Пресенс по дефолту
        self.action = DbAction('client.db')
        self.presence = MyMessMessage(self.socket, {'action': 'presence'})

    def _connect(self):
        # Создать сокет TCP
        sct = socket(AF_INET, SOCK_STREAM)
        # Соединиться с сервером
        sct.connect((self.addr, self.port))
        return sct

    def client_start(self):
        # TODO: надо бы проверки сделать

        # Отправляет пресенс
        self.presence.mess_send()

        # TODO: тесты. Без тестов ничерта не понятно что вернётся и как это проверять дальше
        # Получает респонс
        # Может так не очень верно, но создаёт экземпляр с сокетом для начала...
        listen_sct = MyMessMessage(self.socket)
        # ...далее слушает его. Получает уже очишенные значения от байтов
        response = listen_sct.mess_get

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
                    message = listen_sct.mess_get
                    print(message)
            elif mode == 'w':
                # Пишет
                print('Говорю')
                while True:
                    message_str = input('...> ')
                    # Создаем сообщение по протоколу
                    # Ох, костыли, но работает же
                    msg = MyMessMessage(self.socket, {'action': 'msg', 'message': message_str})
                    # Отправляем на сервер
                    msg.mess_send()
            else:
                print('Нет такого варианта {}'.format(mode))
        # elif presence_response.response == SERVER_ERROR:
        #     print('Внутрення ошибка сервера')
        # elif presence_response.response == WRONG_REQUEST:
        #     print('Неверный запрос на сервер')
        else:
            print('Неверный код ответа от сервера')
