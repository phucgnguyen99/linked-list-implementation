from __future__ import annotations
from dataclasses import dataclass
from typing import Generic, Iterable, Iterator, Optional, TypeVar

T = TypeVar("T")

@dataclass
class Node(Generic[T]):
    value: T
    next: Optional["Node[T]"] = None

class LinkedList(Generic[T]):
    """Singly linked list with a pythonic interface."""

    def __init__(self, iterable: Optional[Iterable[T]] = None) -> None:
        self._head: Optional[Node[T]] = None
        self._tail: Optional[Node[T]] = None
        self._size: int = 0
        if iterable is not None:
            for x in iterable:
                self.append(x)

    # --- basic protocol ---
    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[T]:
        cur = self._head
        while cur is not None:
            yield cur.value
            cur = cur.next

    def __repr__(self) -> str:
        return f"LinkedList({list(self)!r})"

    def __contains__(self, item: T) -> bool:  # enables `in`
        return self.find(item) != -1