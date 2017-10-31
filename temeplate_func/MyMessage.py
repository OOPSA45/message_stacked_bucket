import json
import time

# JIM протокол
from jim.my_jim import MyJimMessage, MyJimResponse

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
        # TODO: тут проверки
        message = MyJimResponse(**self.raw_message, time='Time to kill!')
        self.cur_socket.send(bytes(message))
        return message

    # Умеет получать сообщения
    @property
    def mess_get(self):
        # Получает и сразу декодирует
        message = self.cur_socket.recv(1024)
        message = json.loads(message.decode('utf-8'))
        return message

    def __str__(self):
        return self.raw_message