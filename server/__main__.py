from . import lobby


def main():
    print("server launched")
    server = lobby.LobbyServer(("", 8000))
    server.serve_forever()


if __name__ == '__main__':
    main()
