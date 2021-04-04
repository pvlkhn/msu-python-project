import tkinter
from functools import partial

class GameWindow(tkinter.Frame):
    def __init__(self, game_state, controller, polling_ts, master):
        super().__init__(master=master)

        self.game_field = GameField(game_state, controller, polling_ts, self)

        self.redraw()

    def redraw(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1, uniform="yep")

        self.game_field.redraw()
        self.game_field.grid(row=0, column=0, sticky="NWSE")



class GameField(tkinter.Canvas):
    def __init__(self, game_state, controller, polling_ts, master):
        super().__init__(master=master)

        self.game_state = game_state
        self.bind("<KeyPress>", controller.on_key_pressed)
        self.polling_ts = polling_ts
        self.controller = controller
        self.sync_with_server()


    def redraw(self):
        self.delete("all")

        self.create_rectangle(*self.game_state.get_platform1().get_box())
        self.create_rectangle(*self.game_state.get_platform2().get_box())
        self.create_oval(*self.game_state.get_ball().get_box())


    def sync_with_server(self):
        self.controller.on_sync_with_server()
        self.after(self.polling_ts, self.sync_with_server)