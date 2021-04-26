from .utils import vector_rotation, vector_angle, line_by_vector, clip
from .utils import intersect, normal, line_by_two_points, l2_norm

EPS = 1e-4


def test_vector_rotation():
    d1 = 10
    d2 = -3
    ans = vector_rotation(1.2217, d1, d2)
    ans1 = vector_rotation(2.2217, d1, d2)
    ans2 = vector_rotation(4.2217, d1, d2)
    ans3 = vector_rotation(1.2217, 0, d2)
    assert (abs(ans[0] - 6.2395) < EPS and abs(ans[1] - 8.3706) < EPS)
    assert (abs(ans1[0] + 3.6724) < EPS and abs(ans1[1] - 9.773) < EPS)
    assert (abs(ans2[0] + 7.3583) < EPS and abs(ans2[1] + 7.4063) < EPS)
    assert (abs(ans3[0] - 2.819) < EPS and abs(ans3[1] + 1.0261) < EPS)


def test_vector_angle():
    assert (abs(vector_angle(3, 4, 4, 2) - 0.4636) < EPS)
    assert (abs(vector_angle(3, -4, 4, 2) - 1.7506) < EPS)
    assert (abs(vector_angle(3, 0, 4, 2) - 0.6435) < EPS)
    assert (abs(vector_angle(3, -4, 4, -2) - 2.6779) < EPS)


def test_line_by_vector():
    ans = line_by_vector(0, 0, 1, 1)
    ans1 = line_by_vector(0, 0, 1, -1)
    ans2 = line_by_vector(6, 5, 1, -4)
    ans3 = line_by_vector(6, 5, 1, 0)
    ans4 = line_by_vector(6, 5, 0, 2)
    ans5 = line_by_vector(6, 5, 0, 0)
    assert (abs(ans[0] + 1) < EPS and abs(ans[1] - 1) < EPS and
            abs(ans[2]) < EPS)
    assert (abs(ans1[0] - 1) < EPS and abs(ans1[1] - 1) < EPS and
            abs(ans1[2]) < EPS)
    assert (abs(ans2[0] - 4) < EPS and abs(ans2[1] - 1) < EPS and
            abs(ans2[2] + 29) < EPS)
    assert (abs(ans3[0]) < EPS and abs(ans3[1] - 1) < EPS and
            abs(ans3[2] + 5) < EPS)
    assert (abs(ans4[0] - 1) < EPS and abs(ans4[1]) < EPS and
            abs(ans4[2] + 6) < EPS)
    assert (abs(ans5[0] - 1) < EPS and abs(ans5[1]) < EPS and
            abs(ans5[2] + 6) < EPS)


def test_intersect():
    ans = intersect(1, 2, 3, -4, 5, 0)
    ans1 = intersect(1, 2, 3, -2, 1, -2)
    ans2 = intersect(1, 2, 3, -4, 0, 0)
    try:
        _ = intersect(1, 2, 3, 1, 2, 0)
    except Exception:
        pass
    assert (abs(ans[0] + 1.1538) < EPS and abs(ans[1] + 0.923) < EPS)
    assert (abs(ans1[0] + 1.4) < EPS and abs(ans1[1] + 0.8) < EPS)
    assert (abs(ans2[0]) < EPS and abs(ans2[1] + 1.5) < EPS)


def test_normal():
    ans = normal(0, 1, 2, 3)
    ans1 = normal(0, 1, 4, 0)
    ans2 = normal(-5, 1, 2, 3)
    assert (abs(ans[0] + 1) < EPS and abs(ans[1]) < EPS and
            abs(ans[2] - 2) < EPS)
    assert (abs(ans1[0] + 1) < EPS and abs(ans1[1]) < EPS and
            abs(ans1[2] - 4) < EPS)
    assert (abs(ans2[0] + 1) < EPS and abs(ans2[1] + 5) < EPS and
            abs(ans2[2] - 17) < EPS)


def test_line_by_two_points():
    ans = line_by_two_points(0, 0, 1, 1)
    ans1 = line_by_two_points(0, 0, 1, -1)
    ans2 = line_by_two_points(6, 5, 1, -4)
    ans3 = line_by_two_points(6, 5, 1, 0)
    ans4 = line_by_two_points(6, 5, 0, 2)
    ans5 = line_by_two_points(6, 5, 0, 0)
    assert (abs(ans[0]) < EPS and abs(ans[1]) < EPS and
            abs(ans[2]) < EPS)
    assert (abs(ans1[0] - 2) < EPS and abs(ans1[1]) < EPS and
            abs(ans1[2]) < EPS)
    assert (abs(ans2[0] - 5) < EPS and abs(ans2[1] + 1) < EPS and
            abs(ans2[2] + 29) < EPS)
    assert (abs(ans3[0] - 1) < EPS and abs(ans3[1] + 1) < EPS and
            abs(ans3[2] + 5) < EPS)
    assert (abs(ans4[0] + 2) < EPS and abs(ans4[1] + 1) < EPS and
            abs(ans4[2] - 12) < EPS)
    assert (abs(ans5[0]) < EPS and abs(ans5[1] + 1) < EPS and
            abs(ans5[2]) < EPS)


def test_l2_norm():
    assert (abs(l2_norm([3, 4, 4, 2]) - 6.7082) < EPS)
    assert (abs(l2_norm([3, -4, 54, 2, 5]) - 54.4977) < EPS)


def test_clip():
    assert (abs(clip(3, 4, 6) - 4) < EPS)
    assert (abs(clip(4, 4, 6) - 4) < EPS)
    assert (abs(clip(5, 3, 4) - 4) < EPS)
    try:
        _ = clip(3, 4, 3)
    except AssertionError:
        pass
