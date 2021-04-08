from collections import defaultdict
from copy import deepcopy
import random


class Ball(object):

    RADIUS = 10
    DEFAULT_SPEED = 5

    def __init__(self, pos_x, pos_y):
        self.pos = (pos_x, pos_y)
        self.direction = (0, 0)
        self.moves_count = 0

    def get_pos(self):
        return self.pos

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
        if self.moves_count > 50:
            self.direction = (
                Ball.DEFAULT_SPEED * (random.random() - 0.5),
                Ball.DEFAULT_SPEED * (random.random() - 0.5)
            )
            self.moves_count = 0
        else:
            self.moves_count += 1


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

    def get_pos(self):
        return self.pos

    def get_speed(self):
        return Platform.DEFAULT_SPEED

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
        self.current_frame = 0

    def get_current_frame(self):
        return self.current_frame

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


class HistoryStorage(object):
    MAX_STORED_FRAMES = 600

    def __init__(self):
        self.events_per_frame = defaultdict(list)
        self.do_not_store = set()
        self.states_per_frame = {}
        self.recieved_frames = set()
        self.min_non_recieved_frame = 0

    def add_event(self, frame, event):
        self.events_per_frame[frame].append(event)

    def get_events(self, frame):
        return self.events_per_frame[frame]

    def store_state(self, frame, state):
        self.cleanup()

        self.states_per_frame[frame] = deepcopy(state)
        if len(self.states_per_frame) > HistoryStorage.MAX_STORED_FRAMES:
            print(self.states_per_frame)
            print(self.do_not_store)
            raise RuntimeError("Server doesn't respond for too long")

    def get_game_state(self, frame):
        return self.states_per_frame[frame]

    def cleanup(self):
        while (
            self.min_non_recieved_frame in self.recieved_frames
            and self.min_non_recieved_frame in self.states_per_frame
        ):
            self.recieved_frames.remove(self.min_non_recieved_frame)
            if self.min_non_recieved_frame in self.events_per_frame:
                del self.events_per_frame[self.min_non_recieved_frame]
            del self.states_per_frame[self.min_non_recieved_frame]
            self.min_non_recieved_frame += 1

    def add_recieved_frames(self, frames):
        self.recieved_frames.update(frames)


class NetworkConnection(object):
    def __init__(self):
        pass

    def async_send(self, frame, data):
        pass

    def start_async_read(self):
        pass

    def read_sync(self):
        return []


class NetworkConnectionMock(object):
    def __init__(self, strategy):
        self.strategy = strategy
        self.last_frame = 0

    def async_send(self, frame, data):
        pass

    def start_async_read(self):
        pass

    def read_sync(self):
        frame, moves = self.strategy.get_moves()

        events_by_frames = {
            prev_frame: ['PING']
            for prev_frame in range(self.last_frame, frame)
        }
        events_by_frames[frame] = moves
        self.last_frame = frame + 1

        return events_by_frames
