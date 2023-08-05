def not_none(obj, msg="parameter must not be None"):
    if obj is None:
        raise ValueError(msg)
    else:
        return obj


def safe_get(a_list, index):
    if index < 0 or index > len(a_list)-1:
        raise IndexError("index {} is out of range for {}".format(index, a_list))
    else:
        return a_list[index]
