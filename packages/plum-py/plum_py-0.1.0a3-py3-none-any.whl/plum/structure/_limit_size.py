# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from ._member import Member


def __unpack__(cls, memory, dump, parent):
    sized_member = cls._member

    with memory.limit(parent[sized_member.sizemember] * sized_member.scalefactor):
        return cls.__original_unpack__(memory, dump, None)


class SizedMember(Member):

    __slots__ = [
        'name',
        'cls',
        'sizemember',
        'scalefactor',
    ]

    def __init__(self, sizemember):
        self.sizemember = sizemember
        self.name = None  # assigned during structure class construction
        self.cls = None  # assigned during structure class construction
        self.scalefactor = None  # filled in by finalize

    @property
    def default(self):
        return None

    @property
    def ignore(self):
        return False

    def finalize(self, name, cls, members):
        namespace = {
            '_member': self,
            '__unpack__': classmethod(__unpack__),
            '__original_unpack__': cls.__unpack__,
        }
        self.scalefactor = members[self.sizemember].scalefactor
        cls = type(cls)(cls.__name__, (cls,), namespace)
        super().finalize(name, cls, members)

    def __repr__(self):
        return ('SizedMember('
                f'sizemember={self.sizemember!r},'
                ')')


def limit_size(*, sizemember):
    """Configure structure member to follow size structure member.

    :param str sizemember: size member name
    :returns: structure member definition
    :rtype: SizedMember

    """
    return SizedMember(sizemember)
