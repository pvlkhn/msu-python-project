"""Start a new server hor hosting pong games."""

from . import lobby


def main():
    """Start a new server."""
    print("server launched")
    server = lobby.LobbyServer()
    server.run()


if __name__ == '__main__':
    main()
