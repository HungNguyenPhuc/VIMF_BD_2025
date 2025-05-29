import socket

HOST = "192.168.210.130"
PORT = 29999

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.send(b'popup("Hello, World!")\n')
    s.close()
