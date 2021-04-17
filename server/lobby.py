from random import choices
from string import ascii_lowercase, digits

from flask import Flask, abort, request

from .game import GameServer


class Games:
    def __init__(self, registry_id: str = ""):
        self.registry_id = registry_id
        self.__games = {}

    def get(self, game_id):
        return self.__games.get(game_id, None)

    def get_all(self):
        return list(self.__games.items())

    def add(self, game):
        game_id = self.__new_game_id()
        self.__games[game_id] = game
        return game_id

    def remove(self, game_id):
        del self.__games[game_id]

    def __new_game_id(self):
        def new_uid():
            charset = ascii_lowercase + digits
            return self.registry_id + ''.join(choices(charset, k=32))

        game_id = new_uid()
        while game_id in self.__games:
            game_id = new_uid()
        return game_id


class LobbyServer(Flask):
    def __init__(self, name: str = "Lobby server"):
        super().__init__(name)

        self.games = Games()

        @self.route("/games/")
        def get_all_games():
            return {g_id: get_game(g_id) for g_id, _ in self.games.get_all()}

        @self.route("/games/<game_id>/")
        def get_game(game_id):
            game = self.games.get(game_id)
            if game is None:
                abort(404, description="Game not found")
            return {"port": game.port, "settings": game.settings}

        @self.route("/games/new/", methods=["POST"])
        def create_new_game():
            settings = request.get_json()
            game = GameServer(settings)
            game_id = self.games.add(game)
            game.start()
            return {
                "id": game_id,
                "port": game.port,
                "settings": game.settings
            }
