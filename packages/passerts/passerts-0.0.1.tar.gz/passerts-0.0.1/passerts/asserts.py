def require_not_none(obj):
    if obj is None:
        raise ValueError("parameter must not be None")
    else:
        return obj
