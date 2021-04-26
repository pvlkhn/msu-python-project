import select
import socket
from typing import Optional


class Socket:
    """An abstraction for non-blocking socket"""

    BYTEORDER = "little"
    BUFFER_SIZE = 1024
    SIZE_BYTES = 2

    def __init__(self, sock: Optional[socket.socket] = None):
        """Create a new socket

        :param sock: optional `socket.socket` to build an instance on;
                     if `None` (by default), a new socket is created
        """
        if sock is None:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket = sock
        self.socket.setblocking(False)
        self.__recv_buffer = bytes()

    def connect(self, host: str, port: int, timeout: float) -> None:
        """Connect to remote socket given its hostname and port number

        :param host: string, remote hostname
        :param port: integer, remote port
        :param timeout: connection timeout in seconds, floating-point number
        :return: `None`
        """
        self.socket.settimeout(timeout)
        self.socket.connect((host, port))
        self.socket.settimeout(0)

    def is_connected(self) -> bool:
        """Test if socket currently connected to a remote socket

        :return: `True` if socket is connected to some remote socket,
                 `False` otherwise
        """
        try:
            # When MSG_PEEK is used the data is treated as unread
            # and the next recv shall still return this data
            data = self.socket.recv(self.BUFFER_SIZE, socket.MSG_PEEK)
            if len(data) == 0:
                return False
            return True
        except ConnectionResetError:
            return False

    def send(self, data: bytes) -> None:
        """Send given data to connected remote socket

        :param data: `bytes` object representing data to be sent
        :return: `None`
        """
        size = len(data).to_bytes(self.SIZE_BYTES, self.BYTEORDER)
        message = size + data
        sent = self.socket.send(message)
        # For TCP we don't really need to send all the message bytes
        # in one go, BUT it becomes important if we switch to UDP
        if sent != len(message):
            raise RuntimeError("Unable to send all the data required")

    def recv(self) -> Optional[bytes]:
        """Receive data from connected remote socket

        :return: `bytes` object, if there's any data received,
                 or `None`, otherwise
        """
        ready, _, _ = select.select([self.socket], [], [], 0)
        if len(ready) != 0:
            new_bytes = self.socket.recv(self.BUFFER_SIZE)
            self.__recv_buffer = self.__recv_buffer + new_bytes
        return self.__parse_one_message()

    def __parse_one_message(self) -> Optional[bytes]:
        if len(self.__recv_buffer) == 0:
            return None
        size_bytes = self.__recv_buffer[:self.SIZE_BYTES]
        payload_size = int.from_bytes(size_bytes, self.BYTEORDER)
        message_size = self.SIZE_BYTES + payload_size
        message = self.__recv_buffer[self.SIZE_BYTES:message_size]
        if len(message) < payload_size:
            return None
        self.__recv_buffer = self.__recv_buffer[message_size:]
        return message


class Listener:
    """An abstraction for socket bound and listening on some port"""

    def __init__(self, port: int, backlog: int = 0):
        """Create a new listening socket

        :param port: integer, a port to bind socket to;
                     if 0, a free port will be allocated by OS
        :param backlog: integer, a number of pending unaccepted connections
                        allowed before new incoming connection will fail
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("localhost", port))
        self.socket.listen(backlog)

    def get_host(self) -> str:
        """Returns the hostname that socket is bound to

        :return: the hostname of underlying `socket` object
        """
        return self.socket.getsockname()[0]

    def get_port(self) -> int:
        """Returns the port number that socket is bound to

        :return: the port number of underlying `socket` object
        """
        return int(self.socket.getsockname()[1])

    def accept(self) -> Optional[Socket]:
        """Accepts one pending connection, if there are any

        :return: `Socket` object connecting to some remote socket, if there
                 is at least one connection to accept, or `None`, otherwise
        """
        ready, _, _ = select.select([self.socket], [], [], 0)
        if len(ready) == 0:
            return None
        sock, _ = self.socket.accept()
        return Socket(sock)
