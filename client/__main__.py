from .model import GameState, NetworkConnection
from .view import GameWindow, LobbyBrowserWindow
from .controller import Controller, GameLogicController

import tkinter as tk


class Application(tk.Tk):
    WIDTH = 800
    HEIGHT = 600

    def __init__(self):
        super().__init__()

        game_state = GameState(Application.WIDTH, Application.HEIGHT)
        game_controller = GameLogicController(game_state)
        # TODO: create connection via GUI
        server_connection = NetworkConnection("localhost", 228)
        controller = Controller(
            game_controller=game_controller,
            platform_index=0,  # TODO: use 0 for host, 1 for connected
            server_connection=server_connection
        )

        self.title("Pong game")
        self.minsize(Application.WIDTH, Application.HEIGHT)

        window = GameWindow(game_state, controller, 40, 100, master=self)
        window.pack(expand=True, fill=tk.BOTH)

        # self.lobby_browser = LobbyBrowserWindow(master=self)
        # self.lobby_browser.pack(fill=tk.BOTH)


def main():
    Application().mainloop()


if __name__ == '__main__':
    main()
