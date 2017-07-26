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


def upper_first(symbol):
    """ uppercase first letter """
    name = str(symbol)
    return name[0].upper() + name[1:]


def hash(symbol, hash_type='sha1'):
    """ create a hash code from symbol """
    code = hashlib.new(hash_type)
    code.update(str(symbol).encode('utf-8'))
    return code.hexdigest()


def path(symbol):
    """ replaces '.' with '/' """
    return str(symbol).replace('.', '/')
