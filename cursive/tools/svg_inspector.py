import sys
from pprint import pprint
from util import load_svg, write_svg, to_tuple, to_cnum

if __name__ == '__main__':
    data = load_svg(sys.argv[1])
    print(len(data), 'paths in', sys.argv[1])
    for i, path in enumerate(data):
        nb_curves = len([x for x in path if x.__class__.__name__ != 'Line'])
        nb_lines = len(path) - nb_curves
        print('path', i + 1, '->', nb_curves, 'curves,', nb_lines, 'lines')

        print([x for x in path])
