from .model import GameState, NetworkConnection
from .view import GameWindow, LobbyBrowserWindow
from .controller import Controller, GameLogicController

import tkinter as tk


class Application(tk.Tk):
    WIDTH = 800
    HEIGHT = 600

    def __init__(self):
        super().__init__()
        self.title("Pong game")
        self.minsize(Application.WIDTH, Application.HEIGHT)

        self.frame = tk.Frame(master=self)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self.lobby_browser = LobbyBrowserWindow(
            master=self.frame,
            on_connect=self.on_connect
        )
        self.lobby_browser.grid(row=0, column=0, sticky=tk.NSEW)

        self.game_frame = tk.Frame(master=self.frame)
        self.game_frame.grid(row=0, column=0, sticky=tk.NSEW)

        self.show_lobby()

    def on_connect(self, hostname: str, port: int):
        game_state = GameState(Application.WIDTH, Application.HEIGHT)
        game_controller = GameLogicController(game_state)
        server_connection = NetworkConnection(hostname, port)
        controller = Controller(
            game_controller=game_controller,
            platform_index=0,  # TODO: use 0 for host, 1 for connected
            server_connection=server_connection
        )
        window = GameWindow(controller, 60, 100, master=self.game_frame)
        window.pack(expand=True, fill=tk.BOTH)

        self.show_game()

    def show_game(self):
        self.game_frame.tkraise()

    def show_lobby(self):
        self.lobby_browser.tkraise()


def main():
    Application().mainloop()


if __name__ == '__main__':
    main()
