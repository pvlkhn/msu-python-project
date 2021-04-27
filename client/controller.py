from .model import Controls, GameState, StateCache


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

        if ball.is_intersect(platform0, False) and ball.is_move_to(platform0):
            ball.reflect(platform0, False)
        if ball.is_intersect(platform1, True) and ball.is_move_to(platform1):
            ball.reflect(platform1, True)

        self.move_ball()

        self.inputs = (set(), set())

    def on_input(self, player: int, control: Controls):
        self.inputs[player].add(control)

    def add_score(self, idx):
        self.game_state.scores = (
            self.game_state.scores[0] + (idx == 0),
            self.game_state.scores[1] + (idx == 1)
        )
        self.game_state.reset_ball()

    def add_win(self, idx):
        self.game_state.wins = (
            self.game_state.wins[0] + (idx == 0),
            self.game_state.wins[1] + (idx == 1)
        )
        self.game_state.reset()

    def move_ball(self):
        ball = self.game_state.get_ball()
        ball.move()
        top_left_x, top_left_y, bottom_right_x, bottom_right_y = ball.get_box()

        if bottom_right_y <= 0:
            self.add_score(1)
        elif top_left_y >= self.game_state.window_height:
            self.add_score(0)
        elif top_left_x <= 0 or bottom_right_x >= self.game_state.window_width:
            dir_x, dir_y = ball.get_direction()
            if dir_y > 0:
                self.add_score(0)
            if dir_y < 0:
                self.add_score(1)

        if self.game_state.scores[0] >= GameState.WIN_SCORE:
            self.add_win(0)
        if self.game_state.scores[1] >= GameState.WIN_SCORE:
            self.add_win(1)


class Controller:

    MOVE_KEYSYMS = {
        'Up':    Controls.ROTATE_LEFT,
        'Down':  Controls.ROTATE_RIGHT,
        'Left':  Controls.MOVE_LEFT,
        'Right': Controls.MOVE_RIGHT
    }

    def __init__(self,
                 game_controller: GameLogicController,
                 state_cache: StateCache,
                 platform_index,
                 server_connection):
        self.game_controller = game_controller
        self.state_cache = state_cache
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
        for frame, state in self.server_connection.read():
            self.state_cache.push(state)
        last_state = self.state_cache.pop()
        if last_state is not None:
            self.game_controller.set_game_state(last_state)
