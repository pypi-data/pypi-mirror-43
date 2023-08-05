
from enum import Flag, _decompose
from operator import or_ as _or_
from functools import reduce
from typing import List, Union

from serflag.serflagmeta import SerFlagMeta

class SerFlag (Flag, metaclass=SerFlagMeta):
    '''
    A serializable enum class with two special values ALL and NONE
    None means empty value, i.e. 0
    ALL means a maximum integer with all binary ones possible, i.e. every possible (and yet unthinkable) enum value is contained in ALL.
    This class serializes a enum into a list of strings. If ALL is set, it'll serialize to ['ALL'], otherwise to a list of all enum values contained in self.
    Use deserialize method to deserialize into an OR combination  of flags contained in given string list (or just one flag if its a string)
    User deserialize_destinct method to deserialize string list into a list of flags. This is intended for interopability with platforms that do
    not support enums with binary flags, i.e. GraphQL.
    d
    '''
    def serialize(self) -> List[str]:
        if self.__class__.ALL in self:
            return ['ALL']
        return [k for k, v in self._member_map_.items() if v != self.__class__(0) and v in self]


    @classmethod
    def _create_pseudo_member_(cls, value):
        """
        Create a composite member iff value contains only members.
        Contrary to Flag implementation, don't raise an error if there are extra bits.

        """
        pseudo_member = cls._value2member_map_.get(value, None)
        if pseudo_member is None:
            # construct a singleton enum pseudo-member
            pseudo_member = object.__new__(cls)
            pseudo_member._name_ = None
            pseudo_member._value_ = value
            # use setdefault in case another thread already created a composite
            # with this value
            pseudo_member = cls._value2member_map_.setdefault(value, pseudo_member)
        return pseudo_member


    @classmethod
    def deserialize(cls, value: Union[List[str], str]):
        '''
        Return OR combination of flags contained in value
        '''
        if isinstance(value, str):
            return cls[value]

        if 'ALL' in value:
            return cls.ALL

        return cls(reduce(_or_, (cls[item] for item in value), cls.NONE))

    @classmethod
    def deserialize_distinct(cls, value):
        '''
        Return a list of SerFlag values deserialized from a list of strings.
        Note that ALL will be serialized to all current possible values of enum (i.e. to list of all enum values besides ALL and NONE).
        This is for platforms that do not support binary operations with enums.
        :param value:
        :return:
        '''
        enum_value = cls.deserialize(value)

        return _decompose(cls, enum_value._value_)[0]






