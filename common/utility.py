import pickle
from typing import Optional


def poll(function: callable, stop_value=None):
    """A generator to iterate over values returned by given function

    :param function: a callable with no required arguments to fetch values from
    :param stop_value: a value returned by a callable to stop iteration at
    :return: generator object that iterates over the values returned
             by the given function until it returns given value
    """
    value = function()
    while value != stop_value:
        yield value
        value = function()


def serialize(obj) -> bytes:
    """Serialize object into `bytes`

    :param obj: object to serialize
    :return: `bytes` object
    """
    # TODO: non-pickle serialization
    return pickle.dumps(obj, protocol=4)


def deserialize(data: Optional[bytes]) -> Optional[object]:
    """Deserialize given `bytes` data into python object

    :param data: `bytes` representation of an object
    :return: deserialized object or `None`, if input data is also `None`
    """
    # TODO: non-pickle serialization
    # FIXME current implementation will fail if incorrect data
    #     (non-pickled, for example) is received
    if data is None:
        return None
    return pickle.loads(data)
