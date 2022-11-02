import socket
import threading
import json
import datetime as dt

try:
	f_auth = open('auth.json', 'r+', encoding='utf-8')
	auth = json.load(f_auth)
	f_auth = open('auth.json', 'w+', encoding='utf-8')
except json.decoder.JSONDecodeError:
	auth = {}

except FileNotFoundError:
	f_auth = open('auth.json', 'w+', encoding='utf-8')
	auth = {}

logs = open('logs.txt', 'a')

lock_logs = threading.Lock()

def serv(i):
    global logs
    sock = socket.socket()
    sock.bind(('', 1025 + i))
    print(f'Listening to port {1025 + i}')
    with lock_logs:
        logs.write(f'{dt.datetime.now()} - Listening to port {1025 + i}' + '\n')
        
    while True:
        sock.listen(1)
        conn, addr = sock.accept()
        print(f'Cоединение установлено: {addr[0]}: {addr[1]}')
        with lock_logs:
            logs.write(f'{dt.datetime.now()} - Cоединение установлено: {addr[0]}: {addr[1]}' + '\n')

        if not(addr[0] in auth):
            intro = 'Glad to see you! Please, enter your Name'
            conn.send(intro.encode())
            name = conn.recv(1024)
            auth[addr[0]] = name.decode()
        hello = 'Good afternoon, ' + auth[addr[0]] + '!'
        conn.send(hello.encode())
        print(f'User {auth[addr[0]]} logged in!')
        with lock_logs:
            logs.write(f'{dt.datetime.now()} - Listening to port {1025 + i}' + '\n')
        while True:
            data = conn.recv(1024)
            if data:
                msg = data.decode()
                if msg != 'exit':
                    print(f"Получено от {addr}, user - {auth[addr[0]]}: {msg}")
                    with lock_logs:
                        logs.write(f'{dt.datetime.now()} - Получено от {addr}, user - {auth[addr[0]]}: {msg}' + '\n')
                        logs.write(f'{dt.datetime.now()} - Обратная отправка {msg}' + '\n')
                    conn.send(data)
            if msg == 'exit':
                print(f'Connection with {addr}, user {auth[addr[0]]} closed...')
                with lock_logs:
                    logs.write(f'{dt.datetime.now()} - Connection with {addr}, user {auth[addr[0]]} closed...' + '\n')
                break
        if msg == 'exit':
            break
    print(f'Closing socket, port = {addr[1]}...')
    with lock_logs:
        logs.write(f'{dt.datetime.now()} - Closing socket for user {auth[addr[0]]}, port = {1025 + i}...' + '\n')
    sock.close()

num = int(input("Введите число подключаемых клиентов: "))


threads = [threading.Thread(target = serv, args=[i]) for i in range(num)]
[t1.start() for t1 in threads]
[t1.join() for t1 in threads]
print('Server closed!')
logs.write(f'{dt.datetime.now()} - Server closed!')
json.dump(auth, f_auth, indent='\t')
f_auth.close()
logs.close()
