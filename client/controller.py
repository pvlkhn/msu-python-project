
class Controller:
    def __init__(self, game_state, history_storage, server_connetion):
        self.current_game_state = game_state
        self.history_storage = history_storage
        self.server_connetion = server_connetion

    def on_key_pressed(self, key):
        if will_change_state(key):
            current_frame = self.current_game_state.get_current_frame()
            self.history_storage.add_event(key, current_frame)
            self.server_connetion.async_send(key)

    def on_frame_rendered(self):
        self.on_time_tick(self.game_state)
        current_frame = self.current_game_state.get_current_frame()
        self.states_per_frame.store_state(self.game_state, current_frame)

    def on_time_tick(self, game_state):
        current_frame = game_state.get_current_state()
        events = self.history_storage.get_events(current_frame)
        for event in events:
            if should_move(event):
                game_state.move_ball(event)

        game_state.increment_current_frame()
        return game_state

    def on_sync_with_server(self):
        recieved_events = self.server_connetion.read_sync()
        if len(recieved_events) == 0:
            return
        min_frame = None
        for frame, event in recieved_events:
            self.history_storage.add_event(ts, event)
            if min_frame is None or min_ts < ts:
                min_frame = frame

        game_state = self.history_storage.get_game_state(min_frame)
        self.history_storage.cleanup(min_frame)

        current_frame = self.current_game_state.get_current_frame()
        for frame in range(min_frame, current_frame):
            game_state = on_time_tick(game_state)
            self.history_storage.store(frame, game_state)

        self.game_state = game_state
        self.server_connetion.start_async_read()