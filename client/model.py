from .utils import line_by_two_points, normal, line_by_vector
from .utils import vector_angle, vector_rotation, l2_norm

from math import pi
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
        # platform line
        a1, b1, c1 = line_by_two_points(x1, x2, y1, y2)
        # platform normal
        a2, b2, c2 = normal(a1, b1, ball_center[0], ball_center[1])
        # ball line
        a3, b3, c3 = line_by_vector(ball_center[0], ball_center[1],
                                    self.direction[0], self.direction[1])
        # angle
        alpha = vector_angle(a2, a3, b2, b3)
        a = vector_angle(self.direction[0], x2 - x1,
                         self.direction[1], y2 - y1)
        self.direction = vector_rotation(pi * 2, self.direction[0],
                                         self.direction[1])
        if a < pi / 2:
            self.direction = vector_rotation(-2 * alpha, self.direction[0],
                                             self.direction[1])
        else:
            self.direction = vector_rotation(2 * alpha, self.direction[0],
                                             self.direction[1])

    def is_intersect(self, platform, up):
        ball_center = self.get_pos()
        platform_box = platform.get_box()
        x1, y1, x2, y2 = platform_box[4:8] if up else platform_box[:4]

        distance = (abs((y2 - y1) * ball_center[0] - (x2 - x1) *
                        ball_center[1] + x2 * y1 - x1 * y2) /
                    ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5)

        if vector_angle(x1 - x2, ball_center[0] - x2, y1 - y2,
                        ball_center[1] - y2) > pi / 2:
            distance = l2_norm([y2 - ball_center[1], x2 - ball_center[0]])
        if vector_angle(x2 - x1, ball_center[0] - x1, y2 - y1,
                        ball_center[1] - y1) > pi / 2:
            distance = l2_norm([ball_center[1] - y1, ball_center[0] - x1])

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
        x_tl = x_bl = - Platform.WIDTH / 2
        y_tl = y_tr = - Platform.HEIGHT / 2
        x_tr = x_br = Platform.WIDTH / 2
        y_bl = y_br = Platform.HEIGHT / 2
        x_tl, y_tl = vector_rotation(self.angle, x_tl, y_tl)
        x_tr, y_tr = vector_rotation(self.angle, x_tr, y_tr)
        x_bl, y_bl = vector_rotation(self.angle, x_bl, y_bl)
        x_br, y_br = vector_rotation(self.angle, x_br, y_br)
        x_tl = self.pos[0] + x_tl
        y_tl = self.pos[1] + y_tl
        x_tr = self.pos[0] + x_tr
        y_tr = self.pos[1] + y_tr
        x_bl = self.pos[0] + x_bl
        y_bl = self.pos[1] + y_bl
        x_br = self.pos[0] + x_br
        y_br = self.pos[1] + y_br
        return (x_tl, y_tl, x_tr, y_tr,
                x_br, y_br, x_bl,
                y_bl, x_tl, y_tl)

    def get_pos(self):
        return self.pos

    def move(self, direction: Controls):
        if direction == Controls.MOVE_LEFT:
            self.pos = (self.pos[0] - self.horizontal_speed, self.pos[1])
        elif direction == Controls.MOVE_RIGHT:
            self.pos = (self.pos[0] + self.horizontal_speed, self.pos[1])
        elif direction == Controls.ROTATE_LEFT:
            self.angle += self.rotation_speed
            if self.angle > pi * 2:
                self.angle -= pi * 2
        elif direction == Controls.ROTATE_RIGHT:
            self.angle -= self.rotation_speed
            if self.angle < 0:
                self.angle += pi * 2


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


class NetworkConnection(object):
    def __init__(self, host: str, port: int, timeout: float = 1.0):
        self.socket = Socket()
        self.socket.connect(host, port, timeout)

    def send(self, frame, data):
        self.socket.send(serialize((frame, data)))

    def read(self):
        return [deserialize(e) for e in poll(self.socket.recv)]


class StateCache:
    def __init__(self, size: int):
        self.size = size
        self.states = []

    def push(self, state):
        self.states.append(state)
        self.__shrink()

    def pop(self):
        if len(self.states) == 0:
            return None
        head, self.states = self.states[0], self.states[1:]
        return head

    def __shrink(self):
        starting_index = max(len(self.states) - self.size, 0)
        self.states = self.states[starting_index:]
