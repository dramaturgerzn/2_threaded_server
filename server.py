import socket
import threading
import json

try:
	f_auth = open('auth.json', 'r+', encoding='utf-8')
	auth = json.load(f_auth)
	f_auth = open('auth.json', 'w+', encoding='utf-8')
except json.decoder.JSONDecodeError:
	auth = {}

except FileNotFoundError:
	f_auth = open('auth.json', 'w+', encoding='utf-8')
	auth = {}

def serv(i):
    sock = socket.socket()
    sock.bind(('', 1025 + i))
    while True:
        sock.listen(1)
        conn, addr = sock.accept()
        print(f'Cоединение установлено: {addr[0]}: {addr[1]}')

        if not(addr[0] in auth):
            intro = 'Glad to see you! Please, enter your Name'
            conn.send(intro.encode())
            name = conn.recv(1024)
            auth[addr[0]] = name.decode()
        hello = 'Good afternoon, ' + auth[addr[0]] + '!'
        conn.send(hello.encode())
        print(f'User {auth[addr[0]]} logged in!')
        while True:
            data = conn.recv(1024)
            if data:
                msg = data.decode()
                if msg != 'exit':
                    print(f"Получено от {addr}, user - {auth[addr[0]]}: {msg}")
                    print(f"Обратная отправка {msg}")
                    conn.send(data)
            if msg == 'exit':
                print(f'Connection with {addr}, user {auth[addr[0]]} closed...')
                break
        if msg == 'exit':
            break
    sock.close()

num = int(input("Введите число подключаемых клиентов: "))

threads = [threading.Thread(target = serv, args=[i]) for i in range(num)]
[t1.start() for t1 in threads]
[t1.join() for t1 in threads]
json.dump(auth, f_auth, indent='\t')
f_auth.close()
