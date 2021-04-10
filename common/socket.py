import socket
import select


class Socket:
    BYTEORDER = "little"
    BUFFER_SIZE = 1024
    SIZE_BYTES = 2

    def __init__(self, sock: socket.socket):
        self.socket = sock
        self.socket.setblocking(False)
        self.__recv_buffer = bytes()

    def send(self, data: bytes):
        size = len(data).to_bytes(self.SIZE_BYTES, self.BYTEORDER, signed=False)
        message = size + data
        sent = self.socket.send(message)
        return sent == len(message)

    def recv(self):
        try:
            new_bytes = self.socket.recv(self.BUFFER_SIZE)
            self.__recv_buffer = self.__recv_buffer + new_bytes
            return self.__parse_one_message()
        except BlockingIOError:
            return None

    def __parse_one_message(self):
        if len(self.__recv_buffer) == 0:
            return None
        size_bytes = self.__recv_buffer[:self.SIZE_BYTES]
        payload_size = int.from_bytes(size_bytes, self.BYTEORDER, signed=False)
        message_size = self.SIZE_BYTES + payload_size
        message = self.__recv_buffer[self.SIZE_BYTES:message_size]
        if len(message) < payload_size:
            return None
        self.__recv_buffer = self.__recv_buffer[message_size:]
        return message


class Listener:
    def __init__(self, port: int, backlog: int = 0):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("localhost", port))
        self.socket.listen(backlog)

    def get_port(self):
        return self.socket.getsockname()[1]

    def accept(self):
        ready, _, _ = select.select([self.socket], [], [], 0)
        if len(ready) == 0:
            return None
        sock, _ = self.socket.accept()
        return Socket(sock)
