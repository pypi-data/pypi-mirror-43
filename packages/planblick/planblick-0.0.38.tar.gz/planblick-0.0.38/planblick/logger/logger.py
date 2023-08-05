import socket

def log(message, host="", port=9999):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((host, port))
    try:
        sock.sendall(bytes(message, 'utf-8'))
    finally:
        sock.close()