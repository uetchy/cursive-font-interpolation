import numpy as np
from svg.path import Path, Line, QuadraticBezier, CubicBezier
from util import load_svg, write_svg, to_tuple, to_cnum, intersection, distance


# p1 = origin, p2 = intersection. move p2 with delta distance
def delta_distance(p1, p2, delta=1.0):
    line = np.array([p1, p2])
    dd = distance(*line)
    new_p2_iden = (line[1] - line[0]) / dd
    new_p2 = new_p2_iden * delta * dd + line[0]
    return new_p2


def proportional_interpolate(filename, output='./proportional_interpolation.svg'):
    data = load_svg(filename)

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
    i_curve = CubicBezier(a_curve1.end, to_cnum(
        i_dd1), to_cnum(i_dd2), b_curve1.start)

    j_line1 = (to_tuple(a_curve2.start), to_tuple(a_curve2.control1))
    j_line2 = (to_tuple(b_curve2.end), to_tuple(b_curve2.control2))
    j_intsec = intersection(*j_line1, *j_line2)
    j_dd1 = delta_distance(to_tuple(b_curve2.end), j_intsec, 1.1)
    j_dd2 = delta_distance(to_tuple(a_curve2.start), j_intsec, 1.1)
    j_curve = CubicBezier(b_curve2.end, to_cnum(
        j_dd1), to_cnum(j_dd2), a_curve2.start)

    path = Path(
        Line(a_curve2.start, a_curve1.end),
        i_curve,
        Line(b_curve1.start, b_curve2.end),
        j_curve
    )
    print(path)

    data.append(path)

    write_svg(output, data)


if __name__ == '__main__':
    proportional_interpolate('../datasets/train.svg')
