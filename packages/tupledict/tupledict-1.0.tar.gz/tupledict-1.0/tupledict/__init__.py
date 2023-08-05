"""A multi-key dictionary."""

from collections import defaultdict, UserDict
from itertools import chain


class DictList:
    """List of dictionaries (read-only)."""

    def __init__(self, dicts):
        self._dicts = dicts

    def __getitem__(self, key):
        """Returns a list of entries for the given key in all dictionaries."""
        return [d[key] for d in self._dicts if key in d]

    def values(self):
        """Return all the values in all the dictionaries."""
        return list(chain(*(d.values() for d in self._dicts)))


class TupleDict(UserDict):
    """A dictionary with tuple keys that allows for lookup with key containing wildcard."""

    def __init__(self):
        super().__init__(self)
        self._keysize = None

    def _check_key_size(self, keysize: int, update: bool = False):
        """Update the keysize field or raise and error if the keysize was already set to a different value."""
        if self._keysize is None:
            if update:
                self._keysize = keysize
        elif self._keysize != keysize:
            raise KeyError('Key should have length %d' % self._keysize)

    def _key_to_tuple(self, key):
        if isinstance(key, tuple):
            return key
        else:
            return (key,)
        
    def __setitem__(self, key, value):
        key_t = self._key_to_tuple(key)  # Ensure key is a tuple.
        if None in key_t:
            raise KeyError('Key should not contain None.')
        self._check_key_size(len(key_t), True)
        data = self.data
        for k in key_t[:-1]:
            if k not in data:
                data[k] = {}
            data = data[k]
        data[key_t[-1]] = value
        
    def __getitem__(self, key):
        """Get entries for the given key with wildcards (use None).
        
        If no wildcards are used the result is a single item.
        If wildcards are used the result is a list of items.
        """
        key_t = self._key_to_tuple(key)  # Ensure key is a tuple.
        self._check_key_size(len(key_t))
        data = self.data
        for k in key_t[:-1]:
            if k is None:
                data = DictList(data.values())
            else:
                data = data[k]
        if key_t[-1] is None:
            return list(data.values())
        else:
            return data[key_t[-1]]
    