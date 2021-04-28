"""
Module with helpers.
"""

import os
import pkg_resources
from math import sin, cos, acos
from babel.support import Translations


def load_translations():
    """
    Load translations
    Returns: Translations
    """
    localizations_dir = pkg_resources.resource_filename(
        package_or_requirement='client',
        resource_name='localization'
    )
    return Translations.load(
        dirname=localizations_dir,
        locales=[os.getenv('LC_LANGUAGE'), 'en_US']
    )


def gettext(text, translations=load_translations()):
    """
    Translate text
    Args:
        text (str): text to translate
        translations (Translations): translations
    Returns:
        str
    """
    return translations.gettext(text)


def l2_norm(vec):
    """
    Calculate L2-norm
    Args:
        vec (iterable container): vector
    Returns:
        int or container item type
    """
    result = 0
    for elem in vec:
        result += elem ** 2
    result = result ** 0.5

    return result


def line_by_two_points(x1, x2, y1, y2):
    """
    Calculate line's coefficients by two points
    Args:
        x1 (float): x coordinate of the first point
        x2 (float): x coordinate of the second point
        y1 (float): y coordinate of the first point
        y2 (float): y coordinate of the second point
    Returns:
        a, b, c (tuple of floats): line coefficients
    """
    a = y1 - y2
    b = x2 - x1
    c = x1 * y2 - x2 * y1
    return a, b, c


def normal(a, b, x, y):
    """
    Calculate the line`s normal passing through a point
    Args:
        a (float): first line coefficient
        b (float): second line coefficient
        x (float): x coordinate of the point
        y (float): y coordinate of the point
    Returns:
        a, b, c (tuple of floats): normal's coefficients
    """
    return -b, a, b * x - a * y


def intersect(a, b, c, a1, b1, c1):
    """
    Calculate intersection point of two lines
    Args:
        a (float): first coefficient of the first line
        b (float): second coefficient of the first line
        c (float): third coefficient of the first line
        a1 (float): first coefficient of the second line
        b1 (float): second coefficient of the second line
        c1 (float): third coefficient of the second line
    Returns:
        x,y (tuple of floats): point's coordinates
    """
    if abs(a * b1 - a1 * b) < 1e-10:
        raise ValueError(gettext("Lines are parallel!"))
    x = (c1 * b - c * b1) / (a * b1 - a1 * b)
    y = (a1 * c - a * c1) / (a * b1 - a1 * b)
    return x, y


def line_by_vector(x, y, d1, d2):
    """
    Calculate line's coefficients by point and direction vector
    Args:
        x (float): x coordinate of the point
        y (float): y coordinate of the point
        d1 (float): first vector coordinate
        d2 (float): second vector coordinate
    Returns:
        a, b, c (tuple of floats): line coefficients
    """
    if d1 == 0:
        return 1, 0, -x
    b = 1
    a = -b * d2 / d1
    c = (d2 / d1 * x - y) * b
    return a, b, c


def vector_angle(x1, x2, y1, y2):
    """
    Calculate angle between two vectors
    Args:
        x1 (float): first coordinate of the first vector
        x2 (float): second coordinate of the first vector
        y1 (float): first coordinate of the second vector
        y2 (float): second coordinate of the second vector
    Returns:
        float: angle (in radians)
    """
    a = (x1 * x2 + y1 * y2) / \
        ((x1 ** 2 + y1 ** 2) ** 0.5 * (x2 ** 2 + y2 ** 2) ** 0.5)
    return acos(a)


def vector_rotation(alpha, d1, d2):
    """
    Rotate a vector by an angle
    Args:
        alpha (float): angle in radians
        d1 (float): first vector coordinate
        d2 (float): second vector coordinate
    Returns:
        d1, d2 (tuple of floats): new vector coordinates
    """
    return d1 * cos(alpha) - d2 * sin(alpha), d1 * sin(alpha) + d2 * cos(alpha)
