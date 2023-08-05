"""
Anagram of direg--Dependency Injection REGistry
"""
import inspect
import collections.abc
import functools

__all__ = 'inject', 'registry'


class _Registry(collections.abc.MutableMapping):
    """
    Global registry of identifiers.

    Mapping of names -> values.
    """
    def __init__(self):
        self.factories = {}
        self._instances = {}

    def __getitem__(self, key):
        if key not in self._instances:
            self._instances[key] = self.factories[key]()
        return self._instances[key]

    def __setitem__(self, key, value):
        self._instances[key] = value

    def __len__(self):
        return len(set(self.factories.keys()) | set(self._instances.keys()))

    def __iter__(self):
        yield from set(self.factories.keys()) | set(self._instances.keys())

    def __delitem__(self, key):
        """
        NOTE: Only deletes the instance, NOT the factory. For that, check
        unregister()
        """
        del self._instances[key]

    def register(self, name_or_callable, factory=None):
        """
        r.register(name, callable)
        @r.register
        @r.register(name)

        Register a factory--a type or other callable.

        If no name is given, the __name__ of the factory is used.
        """
        def _(n, f):
            self.factories[n] = f
            return f
        if factory is not None:
            return _(name_or_callable, factory)
        elif callable(name_or_callable):
            return _(name_or_callable.__name__, name_or_callable)
        else:
            return functools.partial(_, name_or_callable)

    def unregister(self, name):
        del self.factories[name]

    def wrap(self, name):
        """
        Wraps the normal factory with the decorated callable. Useful for
        additional application-specific configuration.

        Also supports types and functions, as long as they weren't registered
        with a different name.

        NOTE: Must be called after the factory has been registered.
        """
        if hasattr(name, '__name__'):
            name = name.__name__

        def _(wrapper):
            oldfactory = self.factories[name]

            @functools.wraps(wrapper)
            def newfactory(*pargs, **kwargs):
                inst = oldfactory(*pargs, **kwargs)
                inst = wrapper(inst)
                return inst
            self.factories[name] = newfactory

            # XXX: This could lead to weird behavior?
            if name in self._instances:
                self._instances[name] = wrapper(self._instances[name])

        return _


registry = _Registry()


class inject:
    """
    Resolve an injection.

    Note that this will return to a future--always await it.

    class Spam:
        egg = inject('egg')

        def mymethod(self):
            self.egg.crack()

    As of Python 3.6, the name is optional. If omitted, it will use the name of
    the property.
    """
    def __init__(self, name=None):
        """
        Takes the name of the dependency.

        Also supports types and functions, as long as they weren't registered
        with a different name.
        """
        if hasattr(name, '__name__'):
            name = name.__name__
        self.name = name

    def __set_name__(self, owner, name):
        self.__objclass__ = owner
        if self.name is None:
            self.name = name

    def __get__(self, obj, type=None):
        try:
            return registry[self.name]
        except KeyError:
            raise AttributeError
