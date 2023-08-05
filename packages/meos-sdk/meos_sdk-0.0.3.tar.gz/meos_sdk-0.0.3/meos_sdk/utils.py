import contextlib
from functools import wraps


@contextlib.contextmanager
def monkey_patched(object, name, patch):
    """ Temporarily monkeypatches an object. """

    pre_patched_value = getattr(object, name)
    setattr(object, name, patch)
    yield object
    setattr(object, name, pre_patched_value)


def monkey_patch_decorator(object, name, patch):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            with monkey_patched(object, name, patch):
                return fn(*args, **kwargs)
        return wrapper
    return decorator
