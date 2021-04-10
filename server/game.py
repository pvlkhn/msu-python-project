import pickle
import threading
import time

import common.socket


def poll(function, stop_value=None):
    """:returns generator that calls function until it returns specified value"""
    value = function()
    while value != stop_value:
        yield value
        value = function()


def serialize(obj):
    # TODO: non-pickle serialization
    return pickle.dumps(obj, protocol=4)


def deserialize(data):
    # TODO: non-pickle serialization
    # FIXME current implementation will fail if incorrect data
    #     (non-pickled, for example) is received
    return pickle.loads(data)


# FIXME: this is a mock
# TODO: move game logic to common package
class GameState:
    def __init__(self):
        self.events_processed = 0

    def process(self, events):
        for event in events:
            print(f" -- processing: {event}")
        self.events_processed += len(events)


class GameServer:
    DEFAULT_SETTINGS = {
        "update_interval": 10
    }

    def __init__(self, game_id: str, settings: dict):
        self.id = game_id
        self.settings = self.DEFAULT_SETTINGS
        self.settings.update(settings)
        self.is_running = True
        # port 0 lets OS allocate free port for the socket
        self.__listener = common.socket.Listener(port=0, backlog=2)
        self.__player_sockets = []
        self.__game_state = GameState()
        self.__thread = threading.Thread(target=self.run, name=self.id)
        self.port = self.__listener.get_port()

    def on_tick(self):
        self.__player_sockets.extend(poll(self.__listener.accept))
        for socket in self.__player_sockets:
            events = [deserialize(e) for e in poll(socket.recv)]
            self.__game_state.process(events)
        state = serialize(self.__game_state)
        for socket in self.__player_sockets:
            socket.send(state)

    def start(self):
        self.__thread.start()
        print("asd")

    def run(self):
        while self.is_running:
            self.on_tick()
            # TODO: handle update interval properly
            time.sleep(self.settings["update_interval"])

    def stop(self):
        self.is_running = False
