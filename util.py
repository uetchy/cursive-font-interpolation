import lxml.etree as ET
from svg.path import parse_path


def load_svg(filename):
    doc = ET.parse(filename)
    root = doc.getroot()
    paths = [parse_path(x.attrib['d'])
             for x in root.findall('{http://www.w3.org/2000/svg}path')]
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
