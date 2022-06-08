import socket


# Basic client-side of Python sockets: https://www.geeksforgeeks.org/socket-programming-python/

sock = socket.socket()
port = 7487
sock.connect(('localhost', port))

message = None
while message != '/q':
    received = sock.recv(1024).decode()
    print(received)
    message = input('>')
    sock.send(message.encode())
sock.close()
