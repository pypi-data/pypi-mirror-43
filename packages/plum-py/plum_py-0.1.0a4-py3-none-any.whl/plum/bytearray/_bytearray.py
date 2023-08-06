# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from .._plum import Plum
from ._bytearraytype import ByteArrayType


class ByteArray(bytearray, Plum, metaclass=ByteArrayType):

    """Interpret memory bytes as a byte array.

    .. code-block:: none

        ByteArray(iterable_of_ints) -> bytes array
        ByteArray(string, encoding[, errors]) -> bytes array
        ByteArray(bytes_or_buffer) -> mutable copy of bytes_or_buffer
        ByteArray(int) -> bytes array of size given by the parameter initialized with null bytes
        ByteArray() -> empty bytes array

    """

    # filled in by metaclass
    _nbytes = None

    @classmethod
    def __unpack__(cls, memory, dump, parent):
        nbytes = cls._nbytes

        if nbytes is None:
            nbytes = memory.available

        bytes_ = bytes(memory.consume_bytes(nbytes, dump, cls))

        if dump:
            dump.memory = b''
            for i in range(0, len(memory), 16):
                chunk = memory[i:i + 16]
                subdump = dump.add_level(access=f'[{i}:{i + len(chunk)}]')
                subdump.value = str(list(chunk))
                subdump.memory = chunk

        self = bytearray.__new__(cls, bytes_)
        bytearray.__init__(self, bytes_)

        return self

    @classmethod
    def __pack__(cls, value, dump):

        try:
            dump.cls = cls
        except AttributeError:
            pass  # must be None

        if not isinstance(value, bytes):
            value = bytes(value)

        nbytes = cls._nbytes
        if nbytes is not None and len(value) != nbytes:
            raise ValueError(
                f'expected length to be {nbytes} but instead found {len(value)}')

        if dump:
            for i in range(0, len(value), 16):
                chunk = value[i:i + 16]
                subdump = dump.add_level(access=f'[{i}:{i + len(chunk)}]')
                subdump.value = str(list(chunk))
                subdump.memory = chunk

        yield value

    __repr__ = bytearray.__repr__

    __baserepr__ = __repr__
