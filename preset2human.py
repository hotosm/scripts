# -*- coding:utf-8 -*-
"""
Usage:
    preset2human.py <file> [options]

Options:
    -f, --format <format>        Ouput format: csv, txt, wiki, json [default: txt]
    -o, --output <filepath>      Ouput filepath [default: ./output.txt]
"""

import csv
import codecs

from lxml import etree
from docopt import docopt


class Node(object):

    def __init__(self, node, depth=0, parent=None):
        self._node = node
        self.depth = depth
        self.parent = parent

    @property
    def name(self):
        return self._node.attrib['name']

    @property
    def txt_prefix(self):
        return u""

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__().encode('utf-8')

    @property
    def txt_str(self):
        return self.__unicode__()

    def to_txt(self):
        return "%s%s%s\n" % (
            u"\t" * self.depth,
            self.txt_prefix,
            self.txt_str
        )

    def to_csv(self):
        return ["" for e in range(self.depth)] + [self]

    def to_wiki(self):
        return unicode(self)

    def wiki_key(self, value):
        return u"[[Key:%s|%s]]" % (value, value)

    def wiki_tag(self, key, value):
        return u"[[Tag:%s%%3D%s|%s]]" % (key, value, value)


class GroupNode(Node):

    @property
    def txt_prefix(self):
        return u"— "

    def to_wiki(self):
        affix = u"=" * self.depth
        return u"=%s %s =%s" % (
            affix,
            super(GroupNode, self).to_wiki(),
            affix,
        )


class ItemNode(Node):

    @property
    def txt_prefix(self):
        return u"* "

    def to_wiki(self):
        return u"==== %s ====" % super(ItemNode, self).to_wiki()


class KeyNode(Node):

    @property
    def name(self):
        return self._node.attrib['key']

    @property
    def value(self):
        return self._node.attrib['value']

    @property
    def txt_str(self):
        return u"%s => %s" % (self.name, self.value)

    def to_wiki(self):
        return u"* %s=%s" % (
            self.wiki_key(self.name),
            self.wiki_tag(self.name, self.value)
        )


class ComboNode(Node):

    @property
    def name(self):
        return self._node.attrib['key']

    @property
    def values(self):
        return self._node.attrib['values']

    def to_wiki(self):
        return u"* %s=%s" % (
            self.wiki_key(self.name),
            self.values
        )


class TextNode(Node):

    @property
    def name(self):
        return self._node.attrib['key']

    def __unicode__(self):
        return u"%s => …" % self.name

    def to_wiki(self):
        return u"* %s=…" % (
            self.wiki_key(self.name),
        )


class CheckNode(Node):

    @property
    def name(self):
        return self._node.attrib['key']

    @property
    def default(self):
        try:
            default = self._node.attrib['default']
        except KeyError:
            default = "no"
        finally:
            return default

    @property
    def on(self):
        return self.default in ("yes", "on") and "[yes]" or "yes"

    @property
    def off(self):
        return self.default in ("no", "off") and "[no]" or "no"

    @property
    def txt_str(self):
        return u"%s => %s/%s" % (self.name, self.on, self.off)

    def to_wiki(self):
        return u"* %s=%s/%s" % (
            self.wiki_key(self.name),
            self.on,
            self.off
        )


def main(path):
    with open(path) as f:
        content = f.read()
    content = content.replace('xmlns="', 'xmlnamespace="')
    root = etree.XML(content)
    NODES = []

    def iternode(parent, depth=0):
        for child in parent.getchildren():
            try:
                cls = globals()["%sNode" % child.tag.title()]
            except (AttributeError, KeyError):
                pass
            else:
                node = cls(child, depth)
                NODES.append(node)
            finally:
                iternode(child, depth=depth+1)
    iternode(root)
    return NODES


def to_txt(nodes, filepath):
    content = ""
    for node in nodes:
        content += node.to_txt()
    f = codecs.open(filepath, 'w', "utf-8")
    f.write(content)
    f.close()


def to_csv(nodes, filepath):
    writer = csv.writer(
        open("%s.csv" % filepath, "wb"),
        delimiter=",",
        quotechar='"'
    )
    for node in nodes:
        writer.writerow(node.to_csv())


def to_wiki(nodes, filepath):
    for node in nodes:
        print node.to_wiki()


def to_print(nodes, filepath):
    for node in nodes:
        print node.to_txt()


if __name__ == "__main__":
    args = docopt(__doc__)
    nodes = main(args['<file>'])
    format = args['--format']
    output = args['--output']
    globals()["to_%s" % format](nodes, output)
