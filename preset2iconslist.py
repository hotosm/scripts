"""
Usage:
    preset2iconslist.py <file>
"""
import os
import yaml

from lxml import etree
from docopt import docopt


def extract(filepath):
    with open(filepath) as f:
        content = f.read()
    root = etree.XML(content)
    icons = root.xpath('//*[@icon]')
    ICON = {}
    for icon in icons:
        icon_id = icon.attrib['icon']
        path = os.path.split(icon_id)
        ICON[icon_id] = {
            'path': os.path.join(path[:-1])[0],
            'file_name': path[-1],
            'item_name': icon.attrib['name']
        }
    print yaml.dump(ICON)

if __name__ == "__main__":
    args = docopt(__doc__)
    extract(args['<file>'])
