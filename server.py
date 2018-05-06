from socket import AF_INET, SOCK_STREAM
import socket
import threading
import time
import io
import csv


class MyBytesIO(io.BytesIO):
    def write_end(self, *args, **kwargs):
        _ = super().tell()
        super().seek(0, io.SEEK_END)
        super().write(*args, **kwargs)
        super().seek(_)


class Server:
    def __init__(self, address):
        self.connected = []
        self.received_data = MyBytesIO()

        self.sock = socket.socket(AF_INET, SOCK_STREAM)
        self.sock.bind(address)
        self.sock.listen(5)

        self.players = []

        self.running = True

    def receiver(self, login: str, client_sock: socket.socket):
        while self.running:
            try:
                data = client_sock.recv(1024)
            except ConnectionResetError:
                break

            if data == b'stop':
                print('Client {} stopped'.format(login))
                self.connected.remove(client_sock)
                try:
                    client_sock.sendall(b'')
                except ConnectionResetError:
                    pass
                break

            decoded = data.decode()
            login, command = list(csv.reader(io.StringIO(decoded), delimiter=' ', quotechar='"'))[0]
            if command == 'create':
                self.players.append(login)

            print('Client {} {} sent: "{}"'.format(login, client_sock.getsockname(), decoded))
            self.received_data.write_end(data)
            time.sleep(0.01)

        print('Stopped receiving from {} {}'.format(login, client_sock.getsockname()))
        client_sock.close()

    def sender(self):
        while self.running:
            data = self.received_data.readline()
            if data:
                data = io.StringIO(data.decode().strip())
                login, msg = list(csv.reader(data, delimiter=' ', quotechar='"'))[0]
                msg = '"{}" "{}"\n'.format(login, msg).encode('utf-8')

                for client_sock in self.connected.copy():
                    try:
                        client_sock.sendall(msg)
                    except OSError:
                        self.connected.remove(client_sock)

            time.sleep(0.01)
        print('Stopped sending')

    def shutdown(self):
        self.running = False
        with socket.socket(AF_INET, SOCK_STREAM) as sock:
            sock.connect(self.sock.getsockname())
            sock.sendall(b'stop')
        for client in self.connected:
            client.close()

        self.sock.close()
        print('Shutted down')

    def start(self):
        print('Server thread started')
        threading.Thread(target=self.sender).start()
        while self.running:
            client, addr = self.sock.accept()
            print('Got connection from: {}'.format(addr))

            login = client.recv(1024).decode('utf-8')
            if login == 'stop':
                break
            login = login.split(';;', maxsplit=1)[1]

            for player_login in self.players:
                client.sendall('"{}" "create"\n'.format(player_login).encode())

            self.connected.append(client)
            threading.Thread(target=self.receiver, args=(login, client)).start()
        print('Server thread stopped')


server = Server(('', 50000))

try:
    server.start()

except:
    server.shutdown()
    print('Server stopped')
