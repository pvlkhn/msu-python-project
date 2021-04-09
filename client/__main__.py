from .model import GameState, HistoryStorage, NetworkConnectionMock
from .view import GameWindow
from .controller import Controller, NaiveStrategy

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
        naive_strategy = NaiveStrategy(game_state, player_idx=1)
        server_connetion = NetworkConnectionMock(
            strategy=naive_strategy,
            latency=0.01
        )
        controller = Controller(
            game_state=game_state,
            platform_index=0,  # TODO: use 0 for host, 1 for connected
            history_storage=history_storage,
            server_connetion=server_connetion
        )

        self.title("Pong game")
        self.minsize(Application.WIDTH, Application.HEIGHT)

        window = GameWindow(
            game_state=game_state,
            controller=controller,
            fps=40,
            polling_ts=100,
            master=self
        )
        window.grid(sticky="NWSE")


def main():
    Application().mainloop()


if __name__ == '__main__':
    main()
