from .model import GameState, HistoryStorage, NetworkConnection
from .view import GameWindow
from .controller import Controller

import tkinter


class Application(tkinter.Tk):
    WIDTH = 800
    HEIGHT = 600

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        game_state = GameState(Application.WIDTH, Application.HEIGHT)
        history_storage = HistoryStorage()
        server_connetion = NetworkConnection()
        controller = Controller(
            game_state=game_state,
            platform_index=0,  # TODO: use 0 for host, 1 for connected
            history_storage=history_storage,
            server_connetion=server_connetion
        )

        self.title("Pong game")
        self.minsize(Application.WIDTH, Application.HEIGHT)

        window = GameWindow(game_state, controller, 40, 100, master=self)
        window.grid(sticky="NWSE")


def main():
    Application().mainloop()


if __name__ == '__main__':
    main()
