# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Structure type."""

from .._plum import Plum
from ._structuretype import StructureType


class Structure(dict, Plum, metaclass=StructureType):

    """Interpret memory bytes as a structure with uniquely named and typed members.

    :param mapping: base member values
    :type mapping: dict or iterable of (key, value) pairs
    :param dict kwargs: member values

    """

    # filled in by metaclass
    _ignore = set()
    _members = dict()
    _nbytes = None

    @classmethod
    def __unpack__(cls, memory, dump, parent):
        if dump:
            dump.cls = cls

            self = dict.__new__(cls)
            dict.__init__(self)
            for name, member in cls._members.items():
                subdump = dump.add_level(access=f'.{name}')
                self[member.name] = member.cls.__unpack__(memory, subdump, self)
        else:
            self = dict.__new__(cls)
            dict.__init__(self)
            for name, member in cls._members.items():
                self[member.name] = member.cls.__unpack__(memory, dump, self)

        return self

    @classmethod
    def __pack__(cls, members, dump):
        if not isinstance(members, cls):
            members = cls(members)

        if dump:
            dump.cls = cls

            for name, value in members.items():
                yield from value.__pack__(value, dump.add_level(access=f'.{name}'))
        else:
            for value in members.values():
                yield from value.__pack__(value, dump)

    def __str__(self):
        return f"{{{', '.join(f'{k!r}: {v.__baserepr__()}' for k, v in self.items())}}}"

    __baserepr__ = __str__

    __repr__ = Plum.__repr__  # multiple inheritance - pick the right one

    def __getitem__(self, key):
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            if isinstance(key, int):
                keys = self.keys()
                if 0 <= key < len(keys):
                    key = list(keys)[key]
                else:
                    raise
            else:
                raise

            return dict.__getitem__(self, key)

    def __setitem__(self, key, value):
        if isinstance(key, int):
            keys = self.keys()
            if 0 <= key < len(keys):
                key = list(keys)[key]
            else:
                raise KeyError(key)

        cls = type(self)
        members = cls._members

        if members:
            member = members[key]
            member_cls = member.cls
            if type(value) is not member_cls:
                value = member_cls(value)

        elif not isinstance(value, Plum):
            raise TypeError(f'value must be a plum type instance')

        dict.__setitem__(self, key, value)

    def __delitem__(self, key):
        if self._members:
            raise TypeError(f'{type(self).__name__} does not support deleting members')
        dict.__delitem__(self, key)

    def __getattr__(self, name):
        # facilitate Structures w/o pre-defined members
        try:
            return self[name]
        except KeyError:
            # generate standard AttributeError
            object.__getattribute__(self, name)

    def __setattr__(self, name, value):
        if self._members:
            # this set request is not one of the pre-defined members
            # (member descriptors in class namespace facilitate those),
            # generate standard AttributeError
            object.__getattribute__(self, name)

        self.__setitem__(name, value)

    def __delattr__(self, name):
        self.__delitem__(name)

    def __eq__(self, other):
        if self._ignore:
            me = [(k, v) for k, v in self.items() if k not in self._ignore]
            try:
                iter_items = other.items
            except AttributeError:
                return False
            else:
                other = [(k, v) for k, v in iter_items() if k not in self._ignore]
        else:
            me = list(self.items())
            try:
                iter_items = other.items
            except AttributeError:
                    return False
            else:
                other = list(iter_items())

        return me == other

    def __ne__(self, other):
        return not self.__eq__(other)

    # TODO - implement ignores with compares
