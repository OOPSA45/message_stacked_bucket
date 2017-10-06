from socket import *
import time
import json


# Получает сообщение от клиента
def get_presence(client):
    bpresence = client.recv(1024)
    jpresence = bpresence.decode('utf-8')
    presence = json.loads(jpresence)
    return presence


# Отправляет сообщение клиенту
def send_response(response, client):
    jresponse = json.dumps(response)
    bresponse = jresponse.encode('utf-8')
    client.send(bresponse)


# Форматирует в JIM
def response_format(response_code, time, alert,):
    response = {
        "response": response_code,
        "time": time,
        "alert": alert
    }
    return response


# Формирует ответ клиенту
def presence_parse(presence_message):
    if presence_message['action'] == 'presence':
        response_message = response_format('200', time.time(), 'Presence well done! :: ' + time.ctime(presence_message['time']))
    else:
        response_message = response_format('400', time.time(), 'Unknown query :: ' + time.ctime(presence_message['time']))
    return response_message


if __name__ == '__main__':
    print('Сервер запущен')
    s = socket(AF_INET, SOCK_STREAM)    # Создал сокет TCP
    s.bind(('', 7777))                  # Закрепил адрес
    s.listen(5)                         # Ждёт входящий

    while True:
        client, addr = s.accept()       # Принимает запрос на соединение
        presence_message = get_presence(client)
        print('Получено от клиента {}'.format(presence_message))
        response = presence_parse(presence_message)
        send_response(response, client)
        client.close()



