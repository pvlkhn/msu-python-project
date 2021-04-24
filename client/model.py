from .utils import *

import math
from collections import defaultdict
from copy import deepcopy
from enum import Enum

from common.socket import Socket
from common.utility import serialize, deserialize, poll

Controls = Enum("Controls", [
    "MOVE_LEFT",
    "MOVE_RIGHT",
    "ROTATE_LEFT",
    "ROTATE_RIGHT"
])


class Ball(object):
    RADIUS = 10
    DEFAULT_SPEED = 5

    def __init__(self, pos_x, pos_y):
        self.pos = (pos_x, pos_y)
        self.direction = (0, Ball.DEFAULT_SPEED)

    def get_box(self):
        top_left_x = self.pos[0] - Ball.RADIUS
        top_left_y = self.pos[1] - Ball.RADIUS
        bottom_right_x = self.pos[0] + Ball.RADIUS
        bottom_right_y = self.pos[1] + Ball.RADIUS
        return top_left_x, top_left_y, bottom_right_x, bottom_right_y

    def get_direction(self):
        return self.direction

    def get_pos(self):
        return self.pos

    def move(self):
        self.pos = (
            self.pos[0] + self.direction[0],
            self.pos[1] + self.direction[1]
        )

    def reflect(self, platform, up):
        self.direction = (
            self.direction[0],
            -self.direction[1]
        )
        ball_center = self.get_pos()
        platform_box = platform.get_box()
        x1, y1, x2, y2 = platform_box[4:8] if up else platform_box[:4]
        a1, b1, c1 = line_by_two_points(x1, x2, y1, y2) # platform line
        a2, b2, c2 = normal(a1, b1, ball_center[0], ball_center[1])   # platform normal
        a3, b3, c3 = line_by_vector(ball_center[0], ball_center[1], self.direction[0], self.direction[1])   # ball line
        alpha = math.acos((a2 * a3 + b2 * b3) / (a2 ** 2 + b2 ** 2) ** 0.5 / (a3 ** 2 + b3 ** 2) ** 0.5)    # angle
        a = vector_angle(self.direction[0], x2 - x1, self.direction[1], y2 - y1)
        self.direction = vector_rotation(math.pi * 2, self.direction[0], self.direction[1])
        print(a)
        if a > math.pi / 2:
            self.direction = vector_rotation(-2 * alpha, self.direction[0], self.direction[1])
        else:
            self.direction = vector_rotation(2 * alpha, self.direction[0], self.direction[1])

    def is_intersect(self, platform, up):
        ball_center = self.get_pos()
        platform_box = platform.get_box()
        x1, y1, x2, y2 = platform_box[4:8] if up else platform_box[:4]

        distance = (abs((y2 - y1) * ball_center[0] - (x2 - x1) * ball_center[1] + x2 * y1 - x1 * y2) /
                    ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5)

        if math.acos(((y1 - y2) * (ball_center[1] - y2) + (x1 - x2) * (ball_center[0] - x2)) /
                     ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5 /
                     ((ball_center[0] - x2) ** 2 + (ball_center[1] - y2) ** 2) ** 0.5) > math.pi / 2:
            distance = ((y2 - ball_center[1]) ** 2 + (x2 - ball_center[0]) ** 2) ** 0.5
        if math.acos(((y2 - y1) * (ball_center[1] - y1) + (x2 -x1) * (ball_center[0] - x1)) /
                     ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5 /
                     ((ball_center[0] - x1) ** 2 + (ball_center[1] - y1) ** 2) ** 0.5) > math.pi / 2:
            distance = ((ball_center[1] - y1) ** 2 + (ball_center[0] - x1) ** 2) ** 0.5

        if distance <= Ball.RADIUS:
            return True
        else:
            return False

    def is_move_to(self, platform):
        ball_center = self.get_pos()
        ball_direction = self.get_direction()
        platform_center = platform.get_pos()

        return (platform_center[1] - ball_center[1]) * ball_direction[1] > 0


class Platform(object):
    WIDTH = 100
    HEIGHT = 20
    PADDING = 40
    DEFAULT_SPEED = 5
    DEFAULT_ROTATION = 0.1

    def __init__(self, pos_x, pos_y):
        self.pos = (pos_x, pos_y)
        self.direction = (0, 0)
        self.angle = 0
        self.rotation_speed = Platform.DEFAULT_ROTATION
        self.horizontal_speed = Platform.DEFAULT_SPEED

    def get_box(self):
        top_left_x = - Platform.WIDTH / 2
        top_left_y = - Platform.HEIGHT / 2
        top_right_x = Platform.WIDTH / 2
        top_right_y = - Platform.HEIGHT / 2
        bottom_left_x = - Platform.WIDTH / 2
        bottom_left_y = Platform.HEIGHT / 2
        bottom_right_x = Platform.WIDTH / 2
        bottom_right_y = Platform.HEIGHT / 2
        top_left_x, top_left_y, top_right_x, top_right_y, bottom_left_x, bottom_left_y, bottom_right_x, bottom_right_y = \
            top_left_x * math.cos(self.angle) - top_left_y * math.sin(self.angle), \
            top_left_x * math.sin(self.angle) + top_left_y * math.cos(self.angle), \
            top_right_x * math.cos(self.angle) - top_right_y * math.sin(self.angle), \
            top_right_x * math.sin(self.angle) + top_right_y * math.cos(self.angle), \
            bottom_left_x * math.cos(self.angle) - bottom_left_y * math.sin(self.angle), \
            bottom_left_x * math.sin(self.angle) + bottom_left_y * math.cos(self.angle), \
            bottom_right_x * math.cos(self.angle) - bottom_right_y * math.sin(self.angle),\
            bottom_right_x * math.sin(self.angle) + bottom_right_y * math.cos(self.angle)
        top_left_x = self.pos[0] + top_left_x
        top_left_y = self.pos[1] + top_left_y
        top_right_x = self.pos[0] + top_right_x
        top_right_y = self.pos[1] + top_right_y
        bottom_left_x = self.pos[0] + bottom_left_x
        bottom_left_y = self.pos[1] + bottom_left_y
        bottom_right_x = self.pos[0] + bottom_right_x
        bottom_right_y = self.pos[1] + bottom_right_y
        return top_left_x, top_left_y, top_right_x, top_right_y,bottom_right_x,\
               bottom_right_y, bottom_left_x, bottom_left_y, top_left_x, top_left_y

    def get_pos(self):
        return self.pos

    def move(self, direction: Controls):
        if direction == Controls.MOVE_LEFT:
            self.pos = (self.pos[0] - self.horizontal_speed, self.pos[1])
        elif direction == Controls.MOVE_RIGHT:
            self.pos = (self.pos[0] + self.horizontal_speed, self.pos[1])
        elif direction == Controls.ROTATE_RIGHT:
            self.angle += self.rotation_speed
            if self.angle > math.pi * 2:
                self.angle -= math.pi * 2
        elif direction == Controls.ROTATE_LEFT:
            self.angle -= self.rotation_speed
            if self.angle < 0:
                self.angle += math.pi * 2


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


# TODO: store states only for client-side prediction
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
    def __init__(self, host: str, port: int, timeout: float = 1.0):
        self.socket = Socket()
        self.socket.connect(host, port, timeout)

    def send(self, frame, data):
        self.socket.send(serialize((frame, data)))

    def read(self):
        return [deserialize(e) for e in poll(self.socket.recv)]
