import threading
import time

from common.socket import Listener
from common.utility import serialize, deserialize, poll

from client.model import GameState
from client.controller import GameLogicController


class GameServer:
    DEFAULT_SETTINGS = {
        "name": "yet another game",
        "update_interval": 0.05
    }

    def __init__(self, settings: dict):
        self.settings = self.DEFAULT_SETTINGS
        self.settings.update(settings)
        self.is_running = True
        # port 0 lets OS allocate free port for the socket
        self.__listener = Listener(port=0, backlog=2)
        self.__player_sockets = []
        self.__game_state = GameLogicController(GameState(800, 600))  # FIXME
        self.__thread = threading.Thread(target=self.run)
        self.port = self.__listener.get_port()

    def on_tick(self):
        self.__player_sockets.extend(poll(self.__listener.accept))
        for player, sock in enumerate(self.__player_sockets):
            for event in poll(sock.recv):
                self.__game_state.on_input(player, deserialize(event))
        state = serialize(self.__game_state)
        for sock in self.__player_sockets:
            sock.send(state)

    def start(self):
        self.__thread.start()

    def run(self):
        while self.is_running:
            self.on_tick()
            # TODO: handle update interval properly
            time.sleep(self.settings["update_interval"])

    def stop(self):
        self.is_running = False
