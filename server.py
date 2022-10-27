import socket
import threading

def serv(i):
    sock = socket.socket()
    sock.bind(('', 1025 + i))
    while True:
        sock.listen(1)
        conn, addr = sock.accept()
        print(f'Cоединение установлено: {addr[0]}: {addr[1]}')

        while True:
            data = conn.recv(1024)
                #if not data:
                #break
            if data:
                msg = data.decode()
                print(f"Обратная отправка {msg}")
                conn.send(data)
                print(f"Получено от {addr}: {msg}")
            if msg == 'exit':
                print(f'Соединение разорвано')
                break
        if msg == 'exit':
            print(f'Соединение разорвано')
            break
    sock.close()

num = int(input("Введите число подключаемых клиентов: "))

threads = [threading.Thread(target = serv, args=[i]) for i in range(num)]
[t1.start() for t1 in threads]
