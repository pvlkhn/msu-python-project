from collections import defaultdict


class Ball(object):
    RADIUS = 10

    def __init__(self, pos_x, pos_y):
        self.pos = (pos_x, pos_y)
        self.direction = (0, 1)

    def get_box(self):
        top_left_x = self.pos[0] - Ball.RADIUS
        top_left_y = self.pos[1] - Ball.RADIUS
        bottom_right_x = self.pos[0] + Ball.RADIUS
        bottom_right_y = self.pos[1] + Ball.RADIUS
        return (top_left_x, top_left_y, bottom_right_x, bottom_right_y)


class Platform(object):
    WIDTH = 100
    HEIGHT = 20
    PADDING = 40

    def __init__(self, pos_x, pos_y):
        self.pos = (pos_x, pos_y)
        self.direction = (0, 0)
        self.angle = 0
        self.rotation_speed = 0

    def get_box(self):
        top_left_x = self.pos[0] - Platform.WIDTH / 2
        top_left_y = self.pos[1] - Platform.HEIGHT / 2
        bottom_right_x = self.pos[0] + Platform.WIDTH / 2
        bottom_right_y = self.pos[1] + Platform.HEIGHT / 2
        return (top_left_x, top_left_y, bottom_right_x, bottom_right_y)


class GameState(object):
    def __init__(self, window_width, window_height):
        self.ball = Ball(window_width / 2, window_height / 2)
        self.platform1 = Platform(window_width / 2, window_height - Platform.PADDING)
        self.platform2 = Platform(window_width / 2, Platform.PADDING)
        self.current_frame = 0

    def get_current_frame(self):
        return self.current_frame

    def increment_current_frame(self):
        self.current_frame += 1

    def get_platform1(self):
        return self.platform1

    def get_platform2(self):
        return self.platform2

    def get_ball(self):
        return self.ball


class HistoryStorage(object):
    MAX_STORED_FRAMES = 600

    def __init__(self):
        self.events_per_frame = defaultdict(list)
        self.states_per_frame = {}
        self.min_stored_frame = 0

    def add_event(self, v, event):
        self.events_per_frame[frame].append(event)

    def store_state(self, frame, state):
        self.events_per_frame[frame] = deeepcopy(state)
        if len(self.events_per_frame) > MAX_STORED_FRAMES:
            raise RuntimeError("Server doesn't respond for too long")

    def get_game_state(self, frame):
        return self.events_per_frame[frame]

    def cleanup(self, frame):
        if self.min_stored_frame == frame:
            assert frame in events_per_frame
            assert frame in states_per_frame
            del self.events_per_frame[frame]
            del self.states_per_frame[frame]
            self.min_stored_frame += 1


class NetworkConnection(object):
    def __init__(self):
        pass

    def async_send(self, data):
        pass

    def start_async_read(self):
        pass

    def read_sync(self):
        return []
