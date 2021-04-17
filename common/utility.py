import pickle


def poll(function: callable, stop_value=None):
    value = function()
    while value != stop_value:
        yield value
        value = function()


def serialize(obj):
    # TODO: non-pickle serialization
    return pickle.dumps(obj, protocol=4)


def deserialize(data):
    # TODO: non-pickle serialization
    # FIXME current implementation will fail if incorrect data
    #     (non-pickled, for example) is received
    if data is None:
        return None
    return pickle.loads(data)
