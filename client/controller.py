
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

    def on_frame_rendered(self):
        current_frame = self.current_game_state.get_current_frame()
        events = self.history_storage.get_events(current_frame)
        self.server_connetion.async_send(current_frame, events)
        self.history_storage.store_state(
            frame=current_frame,
            state=self.current_game_state
        )
        self.on_time_tick(self.current_game_state, events)

    @staticmethod
    def on_time_tick(game_state, events):
        game_state.increment_current_frame()
        for platform_index, event in events:
            if event in Controller.MOVE_KEYSYMS:
                game_state.get_platform(platform_index).move(event)

        game_state.get_ball().move()  # TODO: handle intersection

        return game_state

    def convert_keycode_to_move(self, keycode):
        return None

    def on_sync_with_server(self):
        recieved_events = self.server_connetion.read_sync()

        self.server_connetion.start_async_read()
        if len(recieved_events) == 0:
            return

        for frame, events in recieved_events.items():
            for event in events:
                event = (1 - self.platform_index, event)
                self.history_storage.add_event(frame, event)

        self.simulate_lost_events(recieved_events.keys())
        self.history_storage.add_recieved_frames(recieved_events.keys())

    def simulate_lost_events(self, frames):
        min_frame = min(frames)
        current_frame = self.current_game_state.get_current_frame()
        if min_frame < current_frame:
            game_state = self.history_storage.get_game_state(min_frame)
            for frame in range(min_frame, current_frame):
                events = self.history_storage.get_events(frame)
                game_state = self.on_time_tick(game_state, events)
                self.history_storage.store_state(frame + 1, game_state)
            self.current_game_state.copy_from(game_state)


class NaiveStrategy(object):
    def __init__(self, game_state, player_idx):
        self.game_state = game_state
        self.player_idx = player_idx

    def get_moves(self):
        ball_center = self.game_state.get_ball().get_pos()
        platform = self.game_state.get_platform(self.player_idx)
        platform_center = platform.get_pos()
        move_distance = (platform_center[0] - ball_center[0])
        moves_count = move_distance / platform.get_speed()
        frame = self.game_state.get_current_frame()
        if moves_count > -0.5 and moves_count < 0.5:
            return frame, []
        if moves_count > 0:
            return frame, ['Left'] * int(moves_count + 1)
        else:
            return frame, ['Right'] * int(-moves_count + 1)
