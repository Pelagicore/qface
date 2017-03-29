

def merge(a, b, path=None):
    "merges b into a"
    # import pdb; pdb.set_trace()
    path = path or []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            else:
                a[key] = b[key]
        else:
            a[key] = b[key]
    return a
