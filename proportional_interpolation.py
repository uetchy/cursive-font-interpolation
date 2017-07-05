import numpy as np
from svg.path import Path, Line, QuadraticBezier, CubicBezier
from util import load_svg, write_svg, to_tuple, to_cnum


def intersection(p1, p2, p3, p4):
    (x1, y1), (x2, y2) = p1, p2
    (x3, y3), (x4, y4) = p3, p4
    a1 = (y2 - y1) / (x2 - x1)
    a3 = (y4 - y3) / (x4 - x3)
    x = (a1 * x1 - y1 - a3 * x3 + y3) / (a1 - a3)
    y = (y2 - y1) / (x2 - x1) * (x - x1) + y1
    return np.array((x, y))


# returns euclidean distance from p1 to p2
def distance(p1, p2):
    p1, p2 = np.array([p1, p2])
    return np.sqrt(np.sum((p2-p1)**2))


# p1 = origin, p2 = intersection. move p2 with delta distance
def delta_distance(p1, p2, delta=1.0):
    line = np.array([p1, p2])
    dd = distance(*line)
    new_p2_iden = (line[1]-line[0])/dd
    new_p2 = new_p2_iden * delta * dd + line[0]
    return new_p2


if __name__ == '__main__':
    data = load_svg('./train.svg')

    obj1 = data[0]
    obj2 = data[1]

    a_curve1 = obj1[0]  # inversed
    b_curve1 = obj2[1]
    a_curve2 = obj1[2]
    b_curve2 = obj2[3]  # inversed

    # dd = distance(*line)

    i_line1 = (to_tuple(a_curve1.end), to_tuple(a_curve1.control2))
    i_line2 = (to_tuple(b_curve1.start), to_tuple(b_curve1.control1))
    i_intsec = intersection(*i_line1, *i_line2)
    i_dd1 = delta_distance(to_tuple(a_curve1.end), i_intsec, 0.9)
    i_dd2 = delta_distance(to_tuple(b_curve1.start), i_intsec, 0.9)
    print(i_intsec, i_dd1)
    i_curve = CubicBezier(a_curve1.end, to_cnum(i_dd1), to_cnum(i_dd2), b_curve1.start)

    j_line1 = (to_tuple(a_curve2.start), to_tuple(a_curve2.control1))
    j_line2 = (to_tuple(b_curve2.end), to_tuple(b_curve2.control2))
    j_intsec = intersection(*j_line1, *j_line2)
    j_dd1 = delta_distance(to_tuple(b_curve2.end), j_intsec, 1.1)
    j_dd2 = delta_distance(to_tuple(a_curve2.start), j_intsec, 1.1)
    j_curve = CubicBezier(b_curve2.end, to_cnum(j_dd1), to_cnum(j_dd2), a_curve2.start)

    path = Path(
        Line(a_curve2.start, a_curve1.end),
        i_curve,
        Line(b_curve1.start, b_curve2.end),
        j_curve
    )
    print(path)

    data.append(path)

    write_svg('./improved_crossed_interpolation.svg', data)
