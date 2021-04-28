import os
import pkg_resources
from math import sin, cos, acos
from babel.support import Translations


def load_translations():
    localizations_dir = pkg_resources.resource_filename(
        package_or_requirement='client',
        resource_name='localization'
    )
    return Translations.load(
        dirname=localizations_dir,
        locales=[os.getenv('LC_LANGUAGE'), 'en_US']
    )


def gettext(text, translations=load_translations()):
    return translations.gettext(text)


def clip(value, value_min, value_max):
    assert value_min <= value_max
    return max(min(value, value_max), value_min)


def l2_norm(vec):
    result = 0
    for elem in vec:
        result += elem ** 2
    result = result ** 0.5

    return result


def line_by_two_points(x1, x2, y1, y2):
    a = y1 - y2
    b = x2 - x1
    c = x1 * y2 - x2 * y1
    return a, b, c


def normal(a, b, x, y):
    return -b, a, b * x - a * y


def intersect(a, b, c, a1, b1, c1):
    if abs(a * b1 - a1 * b) < 1e-10:
        raise ValueError(gettext("Lines are parallel!"))
    x = (c1 * b - c * b1) / (a * b1 - a1 * b)
    y = (a1 * c - a * c1) / (a * b1 - a1 * b)
    return x, y


def line_by_vector(x, y, d1, d2):
    if d1 == 0:
        return 1, 0, -x
    b = 1
    a = -b * d2 / d1
    c = (d2 / d1 * x - y) * b
    return a, b, c


def vector_angle(x1, x2, y1, y2):
    a = (x1 * x2 + y1 * y2) / \
        ((x1 ** 2 + y1 ** 2) ** 0.5 * (x2 ** 2 + y2 ** 2) ** 0.5)
    return acos(a)


def vector_rotation(alpha, d1, d2):
    return d1 * cos(alpha) - d2 * sin(alpha), d1 * sin(alpha) + d2 * cos(alpha)
