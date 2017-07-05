import numpy as np
import lxml.etree as ET
from svg.path import parse_path

def load_svg(filename):
    doc = ET.parse(filename)
    root = doc.getroot()
    paths = [parse_path(x.attrib['d'])
             for x in root.findall('.//{http://www.w3.org/2000/svg}path')]
    return paths


def write_svg(filename, paths, image_size=(870, 870)):
    str = '<?xml version="1.0" encoding="UTF-8"?>'
    str += f"<svg width=\"{image_size[0]}px\" height=\"{image_size[1]}px\" viewBox=\"0 0 {image_size[0]} {image_size[1]}\" version=\"1.1\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\">"
    for i, path in enumerate(paths):
        str += f"<path d=\"{path.d()}\" id=\"p{i}\"></path>"
    str += '</svg>'

    with open(filename, 'w') as f:
        f.write(str)


def to_tuple(cnum):
    return (cnum.real, cnum.imag)


def to_cnum(tup):
    return complex(tup[0], tup[1])


def to_plain_path(complex_path):
    arr = []
    for point in complex_path:
        point_class = point.__class__.__name__
        if point_class == 'CubicBezier':
            arr.append(
                list(map(to_tuple, [point.start, point.control1, point.control2, point.end])))
        elif point_class == 'Line':
            arr.append(
                list(map(to_tuple, [point.start, point.start, point.end, point.end])))
    return arr


def intersection(p1, p2, p3, p4):
    (x1, y1), (x2, y2) = p1, p2
    (x3, y3), (x4, y4) = p3, p4
    a1 = (y2 - y1) / (x2 - x1)
    a3 = (y4 - y3) / (x4 - x3)
    x = (a1 * x1 - y1 - a3 * x3 + y3) / (a1 - a3)
    y = (y2 - y1) / (x2 - x1) * (x - x1) + y1
    return (x, y)