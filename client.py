import socket
from time import sleep

sock = socket.socket()
sock.setblocking(1)
port = int(input('Введите номер порта: '))
sock.connect(('localhost', port))

while True:
    msg = input()
    sock.send(msg.encode())
    if msg == 'exit':
        break
    data = sock.recv(1024)
    print(f'Данные полученные от сервера: {data.decode()}')
    
    
sock.close()
print('Connection lost.')
