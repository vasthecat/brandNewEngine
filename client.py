from socket import AF_INET, SOCK_STREAM
import socket
import threading
import io


class MyBytesIO(io.BytesIO):
    def write_end(self, *args, **kwargs):
        _ = super().tell()
        super().seek(0, io.SEEK_END)
        super().write(*args, **kwargs)
        super().seek(_)


class NetworkClient:
    def __init__(self, login: str, address):
        self.login = login

        self.socket = socket.socket(AF_INET, SOCK_STREAM)
        self.socket.connect(address)
        self.socket.sendall(b'user;;' + login.encode())

        self.received = MyBytesIO()
        self.running = True

        threading.Thread(target=self.receiver).start()

    def shutdown(self):
        self.running = False
        self.socket.sendall(b'stop')
        self.socket.close()
        print('stopped')

    def receiver(self):
        while self.running:
            try:
                self.received.write_end(self.socket.recv(1024))
            except (ConnectionAbortedError, ConnectionResetError):
                break
        print('stopped receiving')

    def send(self, data):
        if self.running:
            try:
                self.socket.sendall('"{}" "{}"\n'.format(self.login, data).encode())
            except ConnectionResetError:
                return
