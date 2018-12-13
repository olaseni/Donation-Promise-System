class AttrLookup(object):
    def __init__(self, func, instance=None):
        self._func = func
        self._instance = instance

    def __get__(self, instance, owner):
        # Return a new instance of the decorator with the class embedded, rather than
        # store instance here, to avoid race conditions in multithreaded scenarios.
        return AttrLookup(self._func, instance)

    def __getitem__(self, argument):
        return self._func(self._instance, argument)

    def __call__(self, argument=None):
        # When resolving something like {{ user.can.change_number }}, Django will call
        # each element in the dot sequence in order (or otherwise try to access it).
        # When trying to call can(), that will fail, because it expects an extra
        # argument, so Django will fail and leave it at that.
        # If there's no argument passed, we return itself, so Django can continue with
        # the attribute lookup down the chain.
        if argument is None:
            return self
        else:
            return self._func(self._instance, argument)
