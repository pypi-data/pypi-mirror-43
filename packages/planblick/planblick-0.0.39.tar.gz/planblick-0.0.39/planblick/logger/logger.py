import socket

class Logger:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def getLogger(self):
        return self.log

    def log(self, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect((self.host, self.port))
        try:
            sock.sendall(bytes(message, 'utf-8'))
        finally:
            sock.close()
