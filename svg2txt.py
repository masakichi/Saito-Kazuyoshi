# coding: utf-8

import os

from lxml import etree


def gen_all_svg_path():
    for root, dirs, files in os.walk('data'):
        for f in files:
            if f.endswith('.svg'):
                yield os.path.join(root, f)

def svg2txt(path):
    tree = etree.parse(path)
    root = tree.getroot()
    lines = map(lambda e: (e.text or u'').encode('utf-8'), list(root[0]))
    with open(path.replace('svg', 'txt'), 'wb') as f:
        f.write('\n'.join(lines))

def main():
    for path in gen_all_svg_path():
        svg2txt(path)

if __name__ == '__main__':
    main()
