from . import lobby


def main():
    print("server launched")
    server = lobby.LobbyServer()
    server.run()


if __name__ == '__main__':
    main()
