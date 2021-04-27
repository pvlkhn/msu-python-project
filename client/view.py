import tkinter as tk
import requests

from client.controller import Controller


class GameWindow(tk.Frame):
    def __init__(self, controller: Controller, fps: int, master):
        super().__init__(master=master)

        self.game_field = GameField(
            controller=controller,
            fps=fps,
            master=self
        )

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1, uniform="yep")

        self.game_field.redraw()
        self.game_field.grid(row=0, column=0, sticky="NWSE")

        self.focus_set()
        self.bind("<KeyPress>", controller.on_key_pressed)


class GameField(tk.Canvas):
    def __init__(self, controller: Controller, fps: int, master):
        super().__init__(master=master)

        self.controller = controller
        self.fps = fps
        self.polling_ts = int(1000 / self.fps)
        self.start_redrawing()
        self.sync_with_server()

    def redraw(self):
        self.delete("all")
        game_state = self.controller.game_controller.game_state
        platform1 = game_state.get_platform(0).get_box()
        platform2 = game_state.get_platform(1).get_box()
        self.create_line(platform2[4:8], width=1.5)
        self.create_line(platform2)
        self.create_line(platform1[:4], width=1.5)
        self.create_line(platform1[2:])
        self.create_oval(*game_state.get_ball().get_box())

        window_size = game_state.get_window_size()
        scores = game_state.get_scores()
        wins = game_state.get_wins()
        self.create_text(window_size[0] - 100, 22,
                         text='current score:\t' + str(scores[0]),
                         justify=tk.LEFT, font="Verdana 14")
        self.create_text(window_size[0] - 100, 10,
                         text='current wins:\t' + str(wins[0]),
                         justify=tk.LEFT, font="Verdana 14")
        self.create_text(window_size[0] - 100, window_size[1] - 10,
                         text='current score:\t' + str(scores[1]),
                         justify=tk.LEFT, font="Verdana 14")
        self.create_text(window_size[0] - 100, window_size[1] - 22,
                         text='current wins:\t' + str(wins[1]),
                         justify=tk.LEFT, font="Verdana 14")

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

    def __init__(self, master, on_connect: callable):
        super().__init__(master=master)
        self.on_connect = on_connect
        self.games_data = []
        self.server_address = tk.StringVar()
        self.server_address.set("localhost:5000")
        self.server_address_label = tk.Entry(
            master=self,
            textvariable=self.server_address
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
        self.join_game_button = tk.Button(
            master=self,
            text="Join",
            command=self.join_selected_game
        )
        self.server_status = tk.Label(
            master=self,
            text="Checking server status..."
        )

        self.server_address_label.pack(fill=tk.BOTH)
        self.refresh_button.pack(fill=tk.X)
        self.create_game_button.pack(fill=tk.X)
        self.games_list.pack(fill=tk.BOTH)
        self.join_game_button.pack(fill=tk.X)
        self.server_status.pack(fill=tk.X)

        self.__auto_refresh()

    def refresh_games_list(self):
        self.games_list.delete(0, self.games_list.size())
        try:
            response = requests.get(self.make_url("games/")).json()
            self.games_data = list(response.items())
            for game_id, game_data in self.games_data:
                game_name = game_data.get("name", game_id)
                self.games_list.insert(tk.END, game_name)
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

    def join_selected_game(self):
        selection = self.games_list.curselection()
        if selection == ():
            return
        _, game_data = self.games_data[selection[0]]
        game_port = int(game_data["port"])
        self.on_connect(self.get_hostname(), game_port)

    def get_hostname(self):
        return self.server_address.get().split(":")[0].strip()

    def make_url(self, path):
        return self.DEFAULT_SCHEMA + "://" \
             + self.server_address.get() + "/" + path

    def __auto_refresh(self):
        self.refresh_games_list()
        self.after(self.AUTO_REFRESH_INTERVAL * 1000, self.__auto_refresh)
