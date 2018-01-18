import re

translate = None
"""
The translate function used for translating inline tags. The
function will be called with tag, value arguments.

Example:

    import qface.doc

    def qdoc_translate(tag, value):
        return '\\{0}{{{1}}}'.format(tag, value)

    qface.doc.translate = qdoc_translate
"""


class DocObject:
    """
    The documentation object passed into the template engine
    """
    def __init__(self):
        self.brief = []
        self.description = []
        self.see = []
        self.deprecated = False

    def add_tag(self, name, value):
        attr_type = type(getattr(self, name, None))
        if type(value) == str:
            value = self._replace_inline_tags(value)
        if attr_type is bool:
            setattr(self, name, bool(value))
        elif attr_type is str:
            setattr(self, name, str(value))
        elif attr_type is list:
            getattr(self, name).append(value)
        else:
            print('documentation tag @{0} not supported'.format(name))

    @staticmethod
    def _translate(name, value):
        return '{{@{0} {1}}}'.format(name, value)

    @staticmethod
    def _call_translate(mo):
        global translate
        name, value = mo.group(1), mo.group(2)
        translate = translate if translate else DocObject._translate
        return translate(name, value)

    @staticmethod
    def _replace_inline_tags(line):
        return re.sub(r'{@(\w+)\s+([^}]*)}', DocObject._call_translate, line)


def parse_doc(s):
    """ parse a comment in the format of JavaDoc and returns an object, where each JavaDoc tag
        is a property of the object. """
    if not s:
        return
    doc = DocObject()
    tag = None
    s = s[3:-2]  # remove '/**' and '*/'
    for line in s.splitlines():
        line = line.lstrip(' *')  # strip a ' ' and '*' from start
        if not line:
            tag = None  # on empty line reset the tag information
        elif line[0] == '@':
            line = line[1:]
            res = line.split(maxsplit=1)
            if len(res) == 0:
                continue
            tag = res[0]
            if len(res) == 1:
                doc.add_tag(tag, True)
            elif len(res) == 2:
                value = res[1]
                doc.add_tag(tag, value)
        elif tag:  # append to previous matched tag
            doc.add_tag(tag, line)
        else: # append any loose lines to description
            doc.add_tag('description', line)
    return doc
