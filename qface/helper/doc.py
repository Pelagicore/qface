from collections import OrderedDict


def parse_doc(s):
    if not s:
        return
    o = OrderedDict()
    tag = None
    s = s[3:-2]  # remove '/**' and '*/'
    for line in s.splitlines():
        line = line.lstrip(' *')  # strip a ' ' and '*' from start
        if not line:
            tag = None  # on empty line reset the tag information
        elif line[0] == '@':
            line = line[1:]
            res = line.split(maxsplit=1)
            if len(res) == 1:
                tag = res[0]
                o[tag] = True
            elif len(res) == 2:
                tag, value = res[0], res[1]
                o[tag] = value
        elif tag:  # append to previous matched tag
            if type(o[tag]) != list:
                o[tag] = [o[tag]]
            o[tag].append(line)
    return o


def replace_tags(s):
    pass

# {% with doc = parse_doc(symbol.commment) %}
#   \brief {{doc.brief}}
#   \description {{doc.description}}
# {% endwith %}
