import random

from collections import defaultdict
from copy import deepcopy


class Ball(object):

    RADIUS = 10
    DEFAULT_SPEED = 5

    def __init__(self, pos_x, pos_y):
        self.pos = (pos_x, pos_y)

        sign = 1 if random.random() < 0.5 else -1
        self.direction = (0, sign * Ball.DEFAULT_SPEED)

    def get_box(self):
        top_left_x = self.pos[0] - Ball.RADIUS
        top_left_y = self.pos[1] - Ball.RADIUS
        bottom_right_x = self.pos[0] + Ball.RADIUS
        bottom_right_y = self.pos[1] + Ball.RADIUS
        return (top_left_x, top_left_y, bottom_right_x, bottom_right_y)

    def move(self):
        self.pos = (
            self.pos[0] + self.direction[0],
            self.pos[1] + self.direction[1]
        )


class Platform(object):

    WIDTH = 100
    HEIGHT = 20
    PADDING = 40
    DEFAULT_SPEED = 5

    def __init__(self, pos_x, pos_y):
        self.pos = (pos_x, pos_y)
        self.direction = (0, 0)
        self.angle = 0
        self.rotation_speed = 0
        self.horizontal_speed = Platform.DEFAULT_SPEED

    def get_box(self):
        top_left_x = self.pos[0] - Platform.WIDTH / 2
        top_left_y = self.pos[1] - Platform.HEIGHT / 2
        bottom_right_x = self.pos[0] + Platform.WIDTH / 2
        bottom_right_y = self.pos[1] + Platform.HEIGHT / 2
        return (top_left_x, top_left_y, bottom_right_x, bottom_right_y)

    def move(self, direction):
        if direction == 'Left':
            self.pos = (self.pos[0] - self.horizontal_speed, self.pos[1])
        elif direction == 'Right':
            self.pos = (self.pos[0] + self.horizontal_speed, self.pos[1])
        else:
            assert direction in {'Down', 'Up'}  # TODO: implement rotation


class GameState(object):
    def __init__(self, window_width, window_height):
        self.ball = Ball(window_width / 2, window_height / 2)
        self.platform1 = Platform(
            pos_x=(window_width / 2),
            pos_y=(window_height - Platform.PADDING)
        )
        self.platform2 = Platform(
            pos_x=(window_width / 2),
            pos_y=Platform.PADDING
        )
        self.window_width = window_width
        self.window_height = window_height
        self.current_frame = 0
        self.scores = (0, 0)

    def get_current_frame(self):
        return self.current_frame

    def get_scores(self):
        return self.scores

    def get_window_size(self):
        return (self.window_width, self.window_height)

    def increment_current_frame(self):
        self.current_frame += 1

    def get_platform(self, idx):
        assert idx in {0, 1}
        if idx == 0:
            return self.platform1
        else:
            return self.platform2

    def get_ball(self):
        return self.ball

    def move_ball(self):
        self.ball.move()
        ball_box = self.ball.get_box()

        if ball_box[3] <= 0:
            self.scores = (
                self.scores[0],
                self.scores[1] + 1
            )
            self.ball = Ball(self.window_width / 2, self.window_height / 2)

        if ball_box[1] >= self.window_height:
            self.scores = (
                self.scores[0] + 1,
                self.scores[1]
            )
            self.ball = Ball(self.window_width / 2, self.window_height / 2)

class HistoryStorage(object):
    MAX_STORED_FRAMES = 600

    def __init__(self):
        self.events_per_frame = defaultdict(list)
        self.states_per_frame = {}
        self.min_stored_frame = 0

    def add_event(self, frame, event):
        self.events_per_frame[frame].append(event)

    def get_events(self, frame):
        return self.events_per_frame[frame]

    def store_state(self, frame, state):
        self.events_per_frame[frame] = deepcopy(state)
        if len(self.events_per_frame) > HistoryStorage.MAX_STORED_FRAMES:
            raise RuntimeError("Server doesn't respond for too long")

    def get_game_state(self, frame):
        return self.events_per_frame[frame]

    def cleanup(self, frame):
        if self.min_stored_frame == frame:
            assert frame in self.events_per_frame
            assert frame in self.states_per_frame
            del self.events_per_frame[frame]
            del self.states_per_frame[frame]
            self.min_stored_frame += 1


class NetworkConnection(object):
    def __init__(self):
        pass

    def async_send(self, frame, data):
        pass

    def start_async_read(self):
        pass

    def read_sync(self):
        return []
