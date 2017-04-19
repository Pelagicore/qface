import json


def jsonify(obj):
    try:
        # all symbols have a toJson method, try it
        return json.dumps(obj.toJson(), indent='  ')
    except AttributeError:
        pass
    return json.dumps(obj, indent='  ')
