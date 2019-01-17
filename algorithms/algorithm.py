import time
import builtins as __builtin__


class Algorithm:

    time_only = True

    old_print = print

    def __init__(self, node_arr):
        self.node_arr = node_arr
        self.start = 0
        self.end = 0

    @staticmethod
    def class_print(*args, **kwargs):
        """My custom print() function."""
        # Adding new arguments to the print function signature
        # is probably a bad idea.
        # Instead consider testing if custom argument keywords
        # are present in kwargs
        t = '{0:.2f}'.format((time.time() - __class__.__stime__)*1000000)
        if __class__.time_only is True:
            __class__.old_print('{:14s}'.format(f'[{t}us] '), end='')
        else:
            __class__.old_print('{:30s}'.format(f'[{__class__.__cname__} | {t}us] '), end='')
        return __class__.old_print(*args, **kwargs)

    def _process(self, callback):
        global print
        self._callback = callback
        print(
            '\n##########################################################################')
        print(f'Start Algorithm Process [{self.__class__.__name__}]')
        print('##########################################################################')
        __class__.__cname__ = self.__class__.__name__
        old_print = __builtin__.print
        __builtin__.print = self.__class__.class_print
        self.start = time.time()
        __class__.__stime__ = self.start
        self.process(self._run_callback)

    def _run_callback(self):
        global print
        self.end = time.time()
        __builtin__.print = self.__class__.old_print
        print(
            '##########################################################################\n')
        print("Algorithm time: %.2fus" % ((self.end - self.start)*1000000))
        self._callback(self.node_arr)

    def process(self, callback):
        pass

    def _type(self):
        return self.__class__.__name__
