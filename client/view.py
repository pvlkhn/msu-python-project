import tkinter


class GameWindow(tkinter.Frame):
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


class GameField(tkinter.Canvas):
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

        window_size = self.game_state.get_window_size()
        scores = self.game_state.get_scores()
        self.create_text(window_size[0] - 10, 10,
              text=str(scores[0]),
              justify=tkinter.CENTER, font="Verdana 14")
        self.create_text(window_size[0] - 10, window_size[1] - 10,
              text=str(scores[1]),
              justify=tkinter.CENTER, font="Verdana 14")

    def sync_with_server(self):
        self.controller.on_sync_with_server()
        self.after(self.polling_ts, self.sync_with_server)

    def start_redrawing(self):
        self.redraw()
        self.controller.on_frame_rendered()
        self.after(int(1000 / self.fps), self.start_redrawing)
