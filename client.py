import socket
from time import sleep

sock = socket.socket()
sock.setblocking(1)
port = int(input('Введите номер порта: '))
sock.connect(('localhost', port))

data = sock.recv(1024).decode()
print(data)
if 'Glad to see you!' in data:
    name = input('Enter your name: ')
    sock.send(name.encode())
    data = sock.recv(1024).decode()
    print(data)

print('START CHATTING! IF YOU WANT TO END THE CHAT, SEND MESSAGE: `exit`')

while True:
    msg = input()
    sock.send(msg.encode())
    if msg == 'exit':
        break
    data = sock.recv(1024)
    print(f'Данные полученные от сервера: {data.decode()}')
    
    
sock.close()
print('Connection closed.')
