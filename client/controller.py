from .model import Controls, GameState


class GameLogicController:
    def __init__(self, game_state: GameState):
        self.game_state = game_state
        self.inputs = (set(), set())

    def set_game_state(self, game_state):
        self.game_state = game_state

    def on_tick(self):
        self.game_state.increment_current_frame()
        for idx, player_input in enumerate(self.inputs):
            self.game_state.get_platform(idx).move(player_input)
        # TODO: handle intersection
        self.game_state.ball.move()
        self.inputs = (set(), set())

    def on_input(self, player: int, control: Controls):
        self.inputs[player].insert(control)


class Controller:

    MOVE_KEYSYMS = {
        'Up':    Controls.ROTATE_LEFT,
        'Down':  Controls.ROTATE_RIGHT,
        'Left':  Controls.MOVE_LEFT,
        'Right': Controls.MOVE_RIGHT
    }

    def __init__(self, game_controller: GameLogicController, platform_index,
                 server_connection):
        self.game_controller = game_controller
        self.platform_index = platform_index
        self.server_connection = server_connection

    def on_key_pressed(self, event):
        if event.keysym in Controller.MOVE_KEYSYMS:
            current_frame = self.game_controller.game_state.get_current_frame()
            event = (self.platform_index, self.MOVE_KEYSYMS[event.keysym])
            self.server_connection.send(current_frame, event)

    def on_frame_rendered(self):
        pass

    def on_time_tick(self):
        pass

    def on_sync_with_server(self):
        received_states = self.server_connection.read()
        if len(received_states) == 0:
            return
        frame, last_state = received_states[-1]
        self.game_controller.set_game_state(last_state)
