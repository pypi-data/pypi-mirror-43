# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Interpret memory bytes as a floating point number."""

from struct import Struct

from ._floattype import FloatType
from .._plum import Plum


class Float(float, Plum, metaclass=FloatType):

    """Interpret memory bytes as a floating point number.

    :param x: value
    :type x: number or str

    """

    _byteorder = 'little'
    _nbytes = 4
    _pack = Struct('<f').pack
    _unpack = Struct('<f').unpack

    @classmethod
    def __unpack__(cls, memory, dump, parent):
        nbytes = cls._nbytes
        buffer = memory.consume_bytes(nbytes, dump, cls)

        value = cls._unpack(buffer)[0]

        if dump:
            dump.value = value

        return float.__new__(cls, value)

    @classmethod
    def __pack__(cls, value, dump):
        try:
            dump.cls = cls
        except AttributeError:
            pass  # must be None

        bytes_ = cls._pack(value)

        if dump:
            dump.value = value
            dump.memory = bytes_

        yield bytes_

    __baserepr__ = float.__repr__

    __repr__ = Plum.__repr__
