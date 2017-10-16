from messenger import *

if __name__ == '__main__':
    server = MyMessServer()
    while True:
        server.server_accept_in()
