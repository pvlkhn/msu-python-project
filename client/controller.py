
class Controller:

    MOVE_KEYSYMS = {'Up', 'Left', 'Down', 'Right'}
    ACTION_LAG = 5

    def __init__(self, game_state, platform_index,
                 history_storage, server_connetion):
        self.current_game_state = game_state
        self.platform_index = platform_index
        self.history_storage = history_storage
        self.server_connetion = server_connetion

    def on_key_pressed(self, event):
        if event.keysym in Controller.MOVE_KEYSYMS:
            current_frame = self.current_game_state.get_current_frame()
            event = (self.platform_index, event.keysym)
            action_frame = current_frame + Controller.ACTION_LAG
            self.history_storage.add_event(action_frame, event)
            self.server_connetion.async_send(action_frame, event)

    def on_frame_rendered(self):
        current_frame = self.current_game_state.get_current_frame()
        self.on_time_tick(self.current_game_state)
        self.history_storage.store_state(
            frame=current_frame,
            state=self.current_game_state
        )

    def on_time_tick(self, game_state):
        current_frame = game_state.get_current_frame()
        game_state.increment_current_frame()
        events = self.history_storage.get_events(current_frame)
        for platform_index, event in events:
            if event in Controller.MOVE_KEYSYMS:
                game_state.get_platform(self.platform_index).move(event)

        ball = game_state.get_ball()
        platform0 = game_state.get_platform(0)
        platform1 = game_state.get_platform(1)

        if (ball.is_intersect(platform0) and ball.is_move_to(platform0) or 
            ball.is_intersect(platform1) and ball.is_move_to(platform1)):
            ball.reflect()
        ball.move()

        return game_state

    def convert_keycode_to_move(self, keycode):
        return None

    def on_sync_with_server(self):
        recieved_events = self.server_connetion.read_sync()
        if len(recieved_events) == 0:
            return
        min_frame = None
        for frame, event in recieved_events:
            self.history_storage.add_event(frame, event)
            if min_frame is None or min_frame < frame:
                min_frame = frame

        game_state = self.history_storage.get_game_state(min_frame)
        self.history_storage.cleanup(min_frame)

        current_frame = self.current_game_state.get_current_frame()
        for frame in range(min_frame, current_frame):
            game_state = self.on_time_tick(game_state)
            self.history_storage.store(frame, game_state)

        self.game_state = game_state
        self.server_connetion.start_async_read()
