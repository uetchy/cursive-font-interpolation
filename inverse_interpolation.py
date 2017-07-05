import numpy as np
from PIL import Image
from PIL import ImageDraw
from util import load_svg, to_tuple, to_plain_path


# https://stackoverflow.com/a/2292690
def make_bezier(xys):
    # xys should be a sequence of 2-tuples (Bezier control points)
    n = len(xys)
    combinations = pascal_row(n - 1)

    def bezier(ts):
        # This uses the generalized formula for bezier curves
        # http://en.wikipedia.org/wiki/B%C3%A9zier_curve#Generalization
        result = []
        for t in ts:
            tpowers = (t**i for i in range(n))
            upowers = reversed([(1 - t)**i for i in range(n)])
            coefs = [c * a * b for c, a,
                     b in zip(combinations, tpowers, upowers)]
            result.append(
                tuple(sum([coef * p for coef, p in zip(coefs, ps)]) for ps in zip(*xys)))
        return result
    return bezier


def pascal_row(n):
    # This returns the nth row of Pascal's Triangle
    result = [1]
    x, numerator = 1, n
    for denominator in range(1, n // 2 + 1):
        # print(numerator,denominator,x)
        x *= numerator
        x /= denominator
        result.append(x)
        numerator -= 1
    if n & 1 == 0:
        # n is even
        result.extend(reversed(result[:-1]))
    else:
        result.extend(reversed(result))
    return result


if __name__ == '__main__':
    data = load_svg('./train.svg')
    a_path = to_plain_path(data[0])
    b_path = to_plain_path(data[1])

    a_curve1 = a_path[0]
    a_curve2 = a_path[2]

    b_curve1 = b_path[1]
    b_curve2 = b_path[3]

    # m_curve1
    a_curve1_control2, a_curve1_end = np.array(a_curve1[2:])
    b_curve1_start, b_curve1_control1 = np.array(b_curve1[:2])

    m_curve1_start = a_curve1_end
    m_curve1_control1 = a_curve1_end - (a_curve1_control2 - a_curve1_end)
    m_curve1_control2 = b_curve1_start - (b_curve1_control1 - b_curve1_start)
    m_curve1_end = b_curve1_start

    # m_curve2
    a_curve2_start, a_curve2_control1 = np.array(a_curve2[:2])
    b_curve2_control2, b_curve2_end = np.array(b_curve2[2:])

    m_curve2_start = b_curve2_end
    m_curve2_control1 = b_curve2_end - (b_curve2_control2 - b_curve2_end)
    m_curve2_control2 = a_curve2_start - (a_curve2_control1 - a_curve2_start)
    m_curve2_end = a_curve2_start

    # line1
    m_line1_start = m_curve1_end
    m_line1_end = m_curve2_start
    m_line1_control1 = m_line1_start
    m_line1_control2 = m_line1_end

    # line2
    m_line2_start = m_curve2_end
    m_line2_end = m_curve1_start
    m_line2_control1 = m_line2_start
    m_line2_control2 = m_line2_end

    m = [
        list(map(tuple, [m_line1_start, m_line1_control1,
                         m_line1_control2, m_line1_end])),
        list(map(tuple, [m_curve2_start, m_curve2_control1,
                         m_curve2_control2, m_curve2_end])),
        list(map(tuple, [m_line2_start, m_line2_control1,
                         m_line2_control2, m_line2_end])),
        list(map(tuple, [m_curve1_start, m_curve1_control1,
                         m_curve1_control2, m_curve1_end]))
    ]

    # draw_bazier(a_path, image_size=(900, 900))
    im = Image.new('RGBA', (900, 900), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    interval = 100
    ts = [t / float(interval) for t in range(interval + 1)]

    points = []
    for path in a_path:
        bezier = make_bezier(path)
        points.extend(bezier(ts))
    draw.polygon(points, fill='red')

    points = []
    for path in m:
        bezier = make_bezier(path)
        points.extend(bezier(ts))
    draw.polygon(points, fill='blue')

    points = []
    for path in b_path:
        bezier = make_bezier(path)
        points.extend(bezier(ts))
    draw.polygon(points, fill='red')

    im.save('inverse_interpolation.png')
