
class Controller:
    def __init__(self, game_state, history_storage, server_connetion):
        self.current_game_state = game_state
        self.history_storage = history_storage
        self.server_connetion = server_connetion

    def on_key_pressed(self, key):
        print(key)
        if self.should_move(key):
            current_frame = self.current_game_state.get_current_frame()
            self.history_storage.add_event(key, current_frame)
            self.server_connetion.async_send(key)

    def on_frame_rendered(self):
        self.on_time_tick(self.current_game_state)
        current_frame = self.current_game_state.get_current_frame()
        self.history_storage.store_state(self.current_game_state, current_frame)

    def on_time_tick(self, game_state):
        current_frame = game_state.get_current_frame()
        events = self.history_storage.get_events(current_frame)
        for event in events:
            if self.should_move_platform(event):
                game_state.get_current_player_platform()  # TODO: move

        game_state.get_ball().move()  # TODO: handle intersection

        game_state.increment_current_frame()
        return game_state

    def should_move(self, event):
        return True

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
