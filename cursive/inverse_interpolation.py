from svg.path import Line, CubicBezier, Path
from util import load_svg, write_svg


def inverse_interpolate(filename, output='./inverse_interpolation.svg'):
    data = load_svg(filename)

    a_path = data[0]
    b_path = data[1]

    a_curve1 = a_path[0]
    a_curve2 = a_path[2]

    b_curve1 = b_path[1]
    b_curve2 = b_path[3]

    # m_curve1
    m_curve1 = CubicBezier(
        a_curve1.end,
        a_curve1.end - (a_curve1.control2 - a_curve1.end),
        b_curve1.start - (b_curve1.control1 - b_curve1.start),
        b_curve1.start
    )

    # m_curve2
    m_curve2 = CubicBezier(
        b_curve2.end,
        b_curve2.end - (b_curve2.control2 - b_curve2.end),
        a_curve2.start - (a_curve2.control1 - a_curve2.start),
        a_curve2.start
    )

    # line1
    m_line1 = Line(
        m_curve1.end,
        m_curve2.start
    )

    # line2
    m_line2 = Line(
        m_curve2.end,
        m_curve1.start
    )

    path = Path(
        m_line1,
        m_curve2,
        m_line2,
        m_curve1
    )

    data.append(path)

    write_svg(output, data)


if __name__ == '__main__':
    inverse_interpolate('../datasets/train.svg')
