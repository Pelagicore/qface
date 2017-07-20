import json
import hashlib


def jsonify(obj):
    try:
        # all symbols have a toJson method, try it
        return json.dumps(obj.toJson(), indent='  ')
    except AttributeError:
        pass
    return json.dumps(obj, indent='  ')


def upper_first(s):
    s = str(s)
    return s[0].upper() + s[1:]


def hash(s, hash_type='sha1'):
    h = hashlib.new(hash_type)
    h.update(str(s).encode('utf-8'))
    return h.hexdigest()


def path(s):
    return str(s).replace('.', '/')
