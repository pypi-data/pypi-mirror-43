from collections import deque
from copy import deepcopy
# author: thuhak.zhou@nio.com


class Transaction(object):
    """
    run revert functions when exception occurs in context
    """
    def __init__(self):
        self.stack = deque()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def run(self, func, revert_func=None, args=(), kwargs=None, rargs=(), rkwargs=None):
        if kwargs is None:
            kwargs = {}
        if rargs == 'same':
            rargs = args
        if rkwargs is None:
            rkwargs = {}
        elif rkwargs == 'same':
            rkwargs = deepcopy(kwargs)
        try:
            func(*args, **kwargs)
            if revert_func:
                self.stack.appendleft((revert_func, rargs, rkwargs))
        except Exception as e:
            self.rollback()
            raise e

    def rollback(self):
        for revert_func, args, kwargs in self.stack:
            revert_func(*args, **kwargs)
