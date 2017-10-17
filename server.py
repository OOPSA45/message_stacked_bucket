from messenger import *

if __name__ == '__main__':
    server = MyMessServer()
    server.server_socket.serve_forever()
