

def merge(a, b):
    "merges b into a recursively if a and b are dicts"
    for key in b:
        if isinstance(a.get(key), dict) and isinstance(b.get(key), dict):
            merge(a[key], b[key])
        else:
            a[key] = b[key]
    return a
