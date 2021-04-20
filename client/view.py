import tkinter as tk
import requests


class GameWindow(tk.Frame):
    def __init__(self, game_state, controller, fps, polling_ts, master):
        super().__init__(master=master)

        self.game_field = GameField(
            game_state=game_state,
            controller=controller,
            fps=fps,
            polling_ts=polling_ts,
            master=self
        )

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1, uniform="yep")

        self.game_field.redraw()
        self.game_field.grid(row=0, column=0, sticky="NWSE")

        self.focus_set()
        self.bind("<KeyPress>", controller.on_key_pressed)


class GameField(tk.Canvas):
    def __init__(self, game_state, controller, fps, polling_ts, master):
        super().__init__(master=master)

        self.game_state = game_state
        self.polling_ts = polling_ts
        self.controller = controller
        self.sync_with_server()
        self.fps = fps
        self.start_redrawing()

    def redraw(self):
        self.delete("all")

        self.create_rectangle(*self.game_state.get_platform(0).get_box())
        self.create_rectangle(*self.game_state.get_platform(1).get_box())
        self.create_oval(*self.game_state.get_ball().get_box())

    def sync_with_server(self):
        self.controller.on_sync_with_server()
        self.after(self.polling_ts, self.sync_with_server)

    def start_redrawing(self):
        self.redraw()
        self.controller.on_frame_rendered()
        self.after(int(1000 / self.fps), self.start_redrawing)


class LobbyBrowserWindow(tk.Frame):
    DEFAULT_SCHEMA = "http"
    AUTO_REFRESH_INTERVAL = 10

    def __init__(self, master):
        super().__init__(master=master)
        self.server_address = tk.StringVar()
        self.server_address.set("localhost:5000")
        self.server_address_label = tk.Entry(
            master=self,
            textvariable=self.server_address
        )
        self.server_status = tk.Label(
            master=self,
            text="Checking server status..."
        )
        self.refresh_button = tk.Button(
            master=self,
            text="Refresh",
            command=self.refresh_games_list
        )
        self.create_game_button = tk.Button(
            master=self,
            text="Create game",
            command=self.create_game
        )
        self.games_list = tk.Listbox(
            master=self
        )

        self.server_address_label.pack(fill=tk.BOTH)
        self.refresh_button.pack(fill=tk.Y)
        self.create_game_button.pack(fill=tk.Y)
        self.games_list.pack(fill=tk.BOTH)
        self.server_status.pack(fill=tk.Y)

        self.__auto_refresh()

    def refresh_games_list(self):
        self.games_list.delete(0, self.games_list.size())
        try:
            response = requests.get(self.make_url("games/")).json()
            for game_id in response:
                self.games_list.insert(tk.END, game_id)
            self.server_status.config(text="")
        except requests.exceptions.ConnectionError:
            self.server_status.config(text="Could not connect to server!")

    def create_game(self):
        requests.post(
            self.make_url("games/new/"),
            # TODO: customize settings through GUI
            json={"name": "yet another game"}
        )
        self.refresh_games_list()

    def make_url(self, path):
        return self.DEFAULT_SCHEMA + "://" \
             + self.server_address.get() + "/" + path

    def __auto_refresh(self):
        self.refresh_games_list()
        self.after(self.AUTO_REFRESH_INTERVAL * 1000, self.__auto_refresh)
