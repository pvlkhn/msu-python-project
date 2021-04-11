def clip(value, value_min, value_max):
    assert value_min <= value_max
    return max(min(value, value_max), value_min)
    

def l2_norm(vec):
    result = 0
    for elem in vec:
        result += elem ** 2
    result = result ** 0.5

    return result
