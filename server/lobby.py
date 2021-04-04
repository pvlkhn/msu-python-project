from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import re


def endpoint(path):
    # Replace every /{parameter_name} with /(?P<parameter_name>...)
    regexp = re.compile(re.sub(r"/{([^/]+)}", r"/(?P<\1>[^/]+)", path))

    def decorator(function):
        def wrapper(handler, real_path):
            # Create dict { "parameter_name" : parameter_value } from real path
            params = regexp.fullmatch(real_path).groupdict()
            return function(handler, **params)

        setattr(wrapper, "matches", lambda p: regexp.fullmatch(p))
        return wrapper

    return decorator


class LobbyRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)

    def do_GET(self):
        self._set_headers_success()
        for f in [self.get_all_games, self.get_game]:
            if f.matches(self.path):
                self.wfile.write(f(self.path).encode("utf-8"))

    def do_POST(self):
        content_type = self.headers.get_content_type()
        print(content_type)
        if content_type != 'application/json':
            self._set_headers_bad_request()
            return
        message = json.loads(self.rfile.read())
        print(message)
        self._set_headers_success()

    def _set_headers_success(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def _set_headers_bad_request(self):
        self.send_response(400)
        self.end_headers()

    @endpoint("/games/")
    def get_all_games(self):
        return '{ "games": [] }'

    @endpoint("/games/{game_id}")
    def get_game(self, game_id):
        return f'{{ "game_id": {game_id} }}'


class LobbyServer(HTTPServer):
    def __init__(self, server_address):
        super().__init__(server_address, LobbyRequestHandler)
