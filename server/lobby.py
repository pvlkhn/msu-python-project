from random import choices
from string import ascii_uppercase, digits

import flask

from .game import GameServer


class LobbyServer(flask.Flask):
    def __init__(self):
        super().__init__("Lobby server")

        self.__games = {}

        @self.route("/games/")
        def all_games():
            return self.get_all_games()

        @self.route("/games/<game_id>/")
        def game(game_id):
            return self.get_game(game_id)

        @self.route("/games/new/", methods=["POST"])
        def new_game():
            return self.create_game(flask.request.get_json())

    def get_game(self, game_id):
        game = self.__games.get(game_id, None)
        if game is None:
            return None
        return {"port": game.port, "settings": game.settings}

    def get_all_games(self):
        return {g_id: self.get_game(g_id) for g_id in self.__games.keys()}

    def create_game(self, settings):
        def new_id():
            return ''.join(choices(ascii_uppercase + digits, k=32))

        game_id = new_id()
        while game_id in self.__games:
            game_id = new_id()

        game = GameServer(game_id, settings)
        self.__games[game.id] = game
        game.start()
        return {"id": game.id, "port": game.port, "settings": game.settings}
