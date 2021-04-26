import threading
import time

from common.socket import Listener
from common.utility import serialize, deserialize, poll

from client.model import GameState
from client.controller import GameLogicController


class GameServer:
    """Class representing a pong game server"""

    DEFAULT_SETTINGS = {
        "name": "yet another game",
        "update_interval": 1 / 60
    }

    def __init__(self, settings: dict):
        """Creates a new game server

        :param settings: a dictionary with arbitrary game settings
        """
        self.settings = self.DEFAULT_SETTINGS
        self.settings.update(settings)
        self.is_running = True
        # port 0 lets OS allocate free port for the socket
        self.__listener = Listener(port=0, backlog=2)
        self.__player_sockets = []
        self.__player_frames = {}
        self.__game_controller = GameLogicController(GameState(800, 600))
        self.__thread = threading.Thread(target=self.run)
        self.port = self.__listener.get_port()

    def __on_tick(self):
        self.__player_sockets.extend(poll(self.__listener.accept))
        for player, sock in enumerate(self.__player_sockets):
            for event in poll(sock.recv):
                client_frame, player_input = deserialize(event)
                self.__player_frames[player] = max(
                    client_frame,
                    self.__player_frames.get(player, 0)
                )
                self.__game_controller.on_input(player, player_input)
        self.__game_controller.on_tick()
        state = self.__game_controller.game_state
        for player, sock in enumerate(self.__player_sockets):
            message = serialize((self.__player_frames.get(player, 0), state))
            sock.send(message)

    def start(self) -> None:
        """Starts server in separate thread

        :return: `None`
        """
        self.__thread.start()

    def run(self) -> None:
        """Runs server in current thread, returns when the game ends

        :return: `None`
        """
        while self.is_running:
            self.__on_tick()
            # TODO: handle update interval properly
            time.sleep(self.settings["update_interval"])

    def stop(self) -> None:
        """Stops server running in separate thread

        :return: `None`
        """
        self.is_running = False
