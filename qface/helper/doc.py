import re


class DocObject(object):
    pass


def parse_doc(s):
    o = DocObject()
    print('parse_doc:', s)
    if not s:
        return
    tag = None
    for line in s.splitlines():
        if re.match(r'\/\*\*', line):
            continue
        if re.match(r'\s*\*/', line):
            continue
        res = re.match(r'^\s*\*?\s*@(\w+)\s*(.*$)', line)
        if res:
            tag = res.group(1)
            value = res.group(2) if res.group(2) else None
            setattr(o, tag, value)
            continue
        res = re.match(r'\s*\*\s*(.*$)', line)
        if res and tag:
            setattr(o, tag, '{0} {1}'.format(getattr(o, tag), res.group(1)))
    return o

# {% with doc = parse_doc(symbol.commment) %}
#   \brief {{doc.brief}}
#   \description {{doc.description}}
# {% endwith %}
