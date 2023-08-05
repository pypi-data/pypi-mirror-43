# Stubs for zope.interface.common.mapping (Python 3.6)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any, Optional, TypeVar, Generic, Iterable, Iterator
from zope.interface import Interface

KT = TypeVar('KT')
VT = TypeVar('VT')

class IItemMapping(Interface, Generic[KT, VT]):
    def __getitem__(key: KT) -> VT: ...

class IReadMapping(IItemMapping[KT, VT]):
    def get(key: KT, default: Optional[VT] = ...) -> VT: ...
    def __contains__(key: KT) -> bool: ...

class IWriteMapping(Interface, Generic[KT, VT]):
    def __delitem__(key: KT) -> None: ...
    def __setitem__(key: KT, value: VT) -> None: ...

class IEnumerableMapping(IReadMapping[KT, VT]):
    def keys() -> Iterable[KT]: ...
    def __iter__() -> Iterator[VT]: ...
    def values() -> Iterable[VT]: ...
    def items() -> Iterable[tuple[KT, VT]]: ...
    def __len__() -> int: ...

class IMapping(IWriteMapping[KT, VT], IEnumerableMapping[KT, VT]): ...

class IIterableMapping(IEnumerableMapping[KT, VT]):
    def iterkeys() -> Iterable[KT]: ...
    def itervalues() -> Iterable[VT]: ...
    def iteritems() -> Iterable[tuple[KT, VT]]: ...

class IClonableMapping(Interface):
    def copy() -> IClonableMapping: ...

class IExtendedReadMapping(IIterableMapping[KT, VT]):
    def has_key(key: KT) -> bool: ...

class IExtendedWriteMapping(IWriteMapping[KT, VT]):
    def clear() -> None: ...
    def update(d: Any) -> None: ...
    def setdefault(key: KT, default: Optional[VT] = ...) -> None: ...
    def pop(k: KT, *args: Any) -> None: ...
    def popitem() -> VT: ...

class IFullMapping(IExtendedReadMapping[KT, VT], IExtendedWriteMapping[KT, VT], IClonableMapping[KT, VT], IMapping[KT, VT]): ...
