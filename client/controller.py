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
            for control in player_input:
                self.game_state.get_platform(idx).move(control)

        ball = self.game_state.get_ball()
        platform0 = self.game_state.get_platform(0)
        platform1 = self.game_state.get_platform(1)

        if (ball.is_intersect(platform0) and ball.is_move_to(platform0) or
                ball.is_intersect(platform1) and ball.is_move_to(platform1)):
            ball.reflect()
        ball.move()

        self.inputs = (set(), set())

    def on_input(self, player: int, control: Controls):
        self.inputs[player].add(control)


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
            event = self.MOVE_KEYSYMS[event.keysym]
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
