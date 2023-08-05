"""A multi-key dictionary."""

from collections import defaultdict, UserDict
from itertools import chain
from collections.abc import MutableMapping


class MultiKeyDict(UserDict):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._keysize = None 
        
    @property
    def keysize(self):
        return self._keysize
    
    def __len__(self): return len(self.data)
    
    def __getitem__(self, key):
        key_t = self._key_to_tuple(key)
        if self._keysize is not None and len(key_t) != self._keysize:
            raise KeyError("Expected key of length %d, got %s." % (self._keysize, key_t))
        if None in key_t:
            return MKDictView(self, key_t)
        else:
            return super().__getitem__(key)
        
    def _key_to_tuple(self, key):
        if isinstance(key, tuple):
            return key
        else:
            return (key,)
    
    def __setitem__(self, key, item):
        key_t = self._key_to_tuple(key)
        key_l = len(key_t)
        if self._keysize is None:
            self._keysize = key_l
        elif key_l != self._keysize:
            raise KeyError("Expected key of length %d, got %s." % (self._keysize, key_t))
            
        self.data[key_t] = item
    
    def __delitem__(self, key): 
        key_t = self._key_to_tuple(key)
        del self.data[key_t]
    
    # Modify __contains__ to work correctly when __missing__ is present
    def __contains__(self, key):
        key_t = self._key_to_tuple(key)
        return key_t in self.data
        

class MultiKeyDictView(MutableMapping):
    
    def __init__(self, base, selection):
        self._base = base
        self._selection = selection
        
        count_none = sum(1 for x in selection if x is None)
        self._keysize = self._base.keysize - count_none
        
    def _matches(self, key):
        for a, b in zip(key, self._selection):
            if a is not None and b is not None and a != b:
                return False
        return True
    
    def _union(self, key):
        new_key = []
        for a in self._selection:
            if a is None:
                new_key.append(key[0])
                key = key[1:]
            else:
                new_key.append(a)
        return tuple(new_key)
    
    def _filter(self, key):
        new_key = []
        for a, b in zip(self._selection, key):
            if a is None:
                new_key.append(b)
        return tuple(new_key)
        
    def __len__(self): 
        # linear
        s = 0
        for key in iter(self):
            s += 1
        return s
    
    def __getitem__(self, key):
        key_t = self._key_to_tuple(key)
        if len(key_t) != self._keysize:
            raise KeyError("Expected key of length %d, got %s." % (self._keysize, key_t))
            
        union_key = self._union(key_t)
        if None in key_t:
            return MKDictView(self, union_key)
        else:
            return self._base[union_key]

    def __setitem__(self, key, item):
        key_t = self._key_to_tuple(key)
        if len(key_t) != self._keysize:
            raise KeyError("Expected key of length %d, got %s." % (self._keysize, key_t))
        union_key = self._union(key_t)
        self._base.__setitem__(union_key, item)

    def __delitem__(self, key): 
        key_t = self._key_to_tuple(key)
        if len(key_t) != self._keysize:
            raise KeyError("Expected key of length %d, got %s." % (self._keysize, key_t))
        union_key = self._union(key_t)
        del self.data[union_key]
    
    def __iter__(self):
        for base_key in self._base:
            if self._matches(base_key):
                yield self._filter(base_key)

    def __contains__(self, key):
        key_t = self._key_to_tuple(key)
        if len(key_t) != self._keysize:
            return False
        union_key = self._union(key_t)        
        return union_key in self._base

    # Now, add the methods in dicts but not in MutableMapping
    def __repr__(self):
        d = {k: self[k] for k in self}
        return repr(d)
    
    def _key_to_tuple(self, key):
        if isinstance(key, tuple):
            return key
        else:
            return (key,)

    @property
    def keysize(self):
        return self._keysize


    
#     def copy(self):
#         if self.__class__ is UserDict:
#             return UserDict(self.data.copy())
#         import copy
#         data = self.data
#         try:
#             self.data = {}
#             c = copy.copy(self)
#         finally:
#             self.data = data
#         c.update(self)
#         return c
        


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
        super().__init__()
        self._index = {}
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
        self.data[key] = value
        key_t = self._key_to_tuple(key)  # Ensure key is a tuple.
        if None in key_t:
            raise KeyError('Key should not contain None.')
        self._check_key_size(len(key_t), True)
        data = self._index
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
        data = self._index
        for k in key_t[:-1]:
            if k is None:
                data = DictList(data.values())
            else:
                data = data[k]
        if key_t[-1] is None:
            return list(data.values())
        else:
            return data[key_t[-1]]
    