import json
import hashlib


def jsonify(symbol):
    """ returns json format for symbol """
    try:
        # all symbols have a toJson method, try it
        return json.dumps(symbol.toJson(), indent='  ')
    except AttributeError:
        pass
    return json.dumps(symbol, indent='  ')


def upper_first(s):
    """ uppercase first letter """
    s = str(s)
    return s[0].upper() + s[1:]


def lower_first(s):
    s = str(s)
    return s[0].lower() + s[1:]


def hash(symbol, hash_type='sha1'):
    """ create a hash code from symbol """
    code = hashlib.new(hash_type)
    code.update(str(symbol).encode('utf-8'))
    return code.hexdigest()


def path(symbol):
    """ replaces '.' with '/' """
    return str(symbol).replace('.', '/')


filters = {
    'jsonify': jsonify,
    'upper_first': upper_first,
    'lower_first': lower_first,
    'upperfirst': upper_first,
    'lowerfirst': lower_first,
    'hash': hash,
    'path': path,
}
