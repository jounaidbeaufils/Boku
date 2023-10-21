"""module for debugging tools"""
import inspect
import functools
import warnings

def warn_if_called_outside_class(func):
    """Decorator to warn if a method is called outside of its class"""
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        # Check the caller
        frame = inspect.currentframe()
        try:
            outer_frame = frame.f_back
            if outer_frame.f_globals['__name__'] != self.__class__.__module__ or \
               outer_frame.f_locals.get('self', None).__class__ != self.__class__:
                warnings.warn(
                    f"{func.__class__}.{func.__name__} should ideally not be called outside of its class", 
                    RuntimeWarning)
            return func(self, *args, **kwargs)
        finally:
            # Avoid reference cycles
            del frame

    return wrapper

def restrict_to_class(func):
    """Decorator to raise an error if a method is called outside of its class"""
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        # Check the caller
        frame = inspect.currentframe()
        try:
            outer_frame = frame.f_back
            if outer_frame.f_globals['__name__'] != self.__class__.__module__ or \
               outer_frame.f_locals.get('self', None).__class__ != self.__class__:
                raise RuntimeError(f"{func.__class__}.{func.__name__} should not be called outside of its class")
            return func(self, *args, **kwargs)
        finally:
            # Avoid reference cycles
            del frame

    return wrapper
