from svg.path import Path, Line, QuadraticBezier
from util import load_svg, write_svg, to_tuple, to_cnum, intersection


if __name__ == '__main__':
    data = load_svg('./train.svg')

    obj1 = data[0]
    obj2 = data[1]

    a_curve1 = obj1[0]  # inversed
    b_curve1 = obj2[1]
    a_curve2 = obj1[2]
    b_curve2 = obj2[3]  # inversed

    i_line1 = (to_tuple(a_curve1.end), to_tuple(a_curve1.control2))
    i_line2 = (to_tuple(b_curve1.start), to_tuple(b_curve1.control1))
    i_intsec = intersection(*i_line1, *i_line2)
    i_curve = QuadraticBezier(a_curve1.end, to_cnum(i_intsec), b_curve1.start)

    j_line1 = (to_tuple(a_curve2.start), to_tuple(a_curve2.control1))
    j_line2 = (to_tuple(b_curve2.end), to_tuple(b_curve2.control2))
    j_intsec = intersection(*j_line1, *j_line2)
    j_curve = QuadraticBezier(b_curve2.end, to_cnum(j_intsec), a_curve2.start)

    path = Path(
        Line(a_curve2.start, a_curve1.end),
        i_curve,
        Line(b_curve1.start, b_curve2.end),
        j_curve
    )
    print(path)

    data.append(path)

    write_svg('./intersection.svg', data)
