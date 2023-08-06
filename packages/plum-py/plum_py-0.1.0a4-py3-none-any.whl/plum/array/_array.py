# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from .._plum import Plum
from ..int.little import UInt8
from ._arraytype import ArrayType, GREEDY_DIMS


class Array(list, Plum, metaclass=ArrayType):

    """Interpret memory bytes as a list of uniformly typed items.

    :param iterable iterable: items

    """

    # filled in by metaclass
    _dims = GREEDY_DIMS
    _item_cls = UInt8
    _nbytes = None

    @classmethod
    def __unpack__(cls, memory, dump, parent, dims=None, outer_level=True):
        if dims is None:
            dims = cls._dims

        if dump and outer_level:
            dump.cls = cls

        self = list.__new__(cls)
        list.__init__(self)
        self._dims = dims
        self._clsname = cls.__name__ if outer_level else 'Array'

        if dims == GREEDY_DIMS:
            end = memory.nbytes
            i = 0
            item_cls = cls._item_cls
            if dump:
                while memory.consumed < end:
                    subdump = dump.add_level(access=f'[{i}]')
                    list.append(self, item_cls.__unpack__(memory, subdump, self))
                    i += 1
            else:
                while memory.consumed < end:
                    list.append(self, item_cls.__unpack__(memory, None, self))
                    i += 1
        elif None in dims:
            raise RuntimeError('unpack does not support multidimensional greedy arrays')
        else:
            itemdims = dims[1:]
            if dump:
                if itemdims:
                    for i in range(dims[0]):
                        subdump = dump.add_level(access=f'[{i}]')
                        list.append(self, cls.__unpack__(memory, subdump, self, itemdims, False))
                else:
                    item_cls = cls._item_cls
                    for i in range(dims[0]):
                        subdump = dump.add_level(access=f'[{i}]')
                        list.append(self, item_cls.__unpack__(memory, subdump, self))
            else:
                if itemdims:
                    for i in range(dims[0]):
                        list.append(self, cls.__unpack__(memory, None, self, itemdims, False))
                else:
                    item_cls = cls._item_cls
                    for i in range(dims[0]):
                        list.append(self, item_cls.__unpack__(memory, None, self))

        return self

    @classmethod
    def __pack__(cls, items, dump, dims=None, outer_level=True):
        if not isinstance(items, cls):
            items = cls(items)

        if dims is None:
            dims = items._dims

        itemdims = dims[1:]

        if dump:
            if outer_level:
                dump.cls = cls

            if itemdims:
                for i, item in enumerate(items):
                    yield from item.__pack__(item, dump.add_level(access=f'[{i}]'), itemdims, False)
            else:
                for i, item in enumerate(items):
                    yield from item.__pack__(item, dump.add_level(access=f'[{i}]'))
        else:
            if itemdims:
                for item in items:
                    yield from item.__pack__(item, None, itemdims, False)
            else:
                for item in items:
                    yield from item.__pack__(item, None)

    def __str__(self):
        return f'[{", ".join(item.__baserepr__() for item in self)}]'

    __baserepr__ = __str__

    def __repr__(self):
        return f'{self._clsname}({self.__baserepr__()})'

    def __setitem__(self, index, item):
        # FUTURE: add mechanism to keep track of index for arrays
        cls = type(self)

        if isinstance(index, slice):
            items = list(item)
            replace_count = len(self[index])
            if len(items) != replace_count:
                raise ValueError(f'{cls.__name__!r} object does not support resizing')
            for i, item in zip(range(len(self))[index], items):
                self[i] = item
        else:
            item_dims = self._dims[1:]
            if item_dims:
                if (type(item) is not cls) or (item._dims != item_dims):
                    item = cls._make_instance(item, item_dims)
            else:
                if type(item) is not cls._item_cls:
                    item = cls._item_cls(item)

            list.__setitem__(self, index, item)

    def append(self, item):
        cls = type(self)
        raise TypeError(f'{cls.__name__!r} object does not support resizing)')

    def clear(self):
        cls = type(self)
        raise TypeError(f'{cls.__name__!r} object does not support resizing)')

    def extend(self, iterable):
        cls = type(self)
        raise TypeError(f'{cls.__name__!r} object does not support resizing)')

    def insert(self, index, item):
        cls = type(self)
        raise TypeError(f'{cls.__name__!r} object does not support resizing)')

    def pop(self, index=-1):
        cls = type(self)
        raise TypeError(f'{cls.__name__!r} object does not support resizing)')

    def remove(self, value):
        cls = type(self)
        raise TypeError(f'{cls.__name__!r} object does not support resizing)')
