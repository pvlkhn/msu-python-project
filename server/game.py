import pickle
import time

import network.socket


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
    return pickle.loads(data)


# FIXME: this is a mock
# TODO: move game logic to common package
class GameState:
    def __init__(self, settings):
        self.settings = settings
        self.events_processed = 0

    def process(self, events):
        self.events_processed += len(events)


class GameServer:
    def __init__(self, settings):
        self.settings = settings
        self.is_running = True
        # port 0 lets OS allocate free port for the socket
        self.__listener = network.socket.Listener(port=0, backlog=2)
        self.__player_sockets = []
        self.__game_state = GameState(settings)

    def get_port(self):
        return self.__listener.get_port()

    def on_tick(self):
        self.__player_sockets.extend(poll(self.__listener.accept))
        for socket in self.__player_sockets:
            events = [deserialize(e) for e in poll(socket.revc)]
            self.__game_state.process(events)
        state = serialize(self.__game_state)
        for socket in self.__player_sockets:
            socket.send(state)

    def run(self, update_interval):
        while self.is_running:
            self.on_tick()
            # TODO: handle update interval properly
            time.sleep(update_interval)

    def stop(self):
        self.is_running = False
