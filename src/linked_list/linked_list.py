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

    # --- helpers ---
    def _node_at(self, index: int) -> Node[T]:
        """Return the node at a non-negative index. Raises IndexError if OOB."""
        if index < 0 or index >= self._size:
            raise IndexError("index out of range")
        cur = self._head
        for _ in range(index):
            assert cur is not None  # for type-checkers
            cur = cur.next
        assert cur is not None
        return cur

    # --- core operations ---
    def append(self, value: T) -> None:
        """Insert at tail."""
        new = Node(value)
        if self._tail is None:  # empty
            self._head = self._tail = new
        else:
            self._tail.next = new
            self._tail = new
        self._size += 1

    def prepend(self, value: T) -> None:
        """Insert at head."""
        new = Node(value, next=self._head)
        self._head = new
        if self._tail is None:  # was empty
            self._tail = new
        self._size += 1

    def insert(self, index: int, value: T) -> None:
        """Insert before position index (0..len). index == len appends.
        Negative indexes are not supported for simplicity.
        """
        if index < 0 or index > self._size:
            raise IndexError("index out of range")
        if index == 0:
            self.prepend(value)
            return
        if index == self._size:
            self.append(value)
            return
        prev = self._node_at(index - 1)
        new = Node(value, next=prev.next)
        prev.next = new
        self._size += 1

    def pop(self, index: int = -1) -> T:
        """Remove and return item at index (default last)."""
        if self._size == 0:
            raise IndexError("pop from empty LinkedList")
        if index == -1:
            index = self._size - 1
        if index < 0 or index >= self._size:
            raise IndexError("index out of range")
        if index == 0:
            assert self._head is not None
            value = self._head.value
            self._head = self._head.next
            if self._head is None:
                self._tail = None
            self._size -= 1
            return value
        prev = self._node_at(index - 1)
        assert prev.next is not None
        value = prev.next.value
        prev.next = prev.next.next
        if index == self._size - 1:
            self._tail = prev
        self._size -= 1
        return value

    def remove(self, value: T) -> None:
        """Remove first occurrence of value. Raises ValueError if not found."""
        prev: Optional[Node[T]] = None
        cur = self._head
        while cur is not None:
            if cur.value == value:
                if prev is None:  # removing head
                    self._head = cur.next
                    if self._head is None:
                        self._tail = None
                else:
                    prev.next = cur.next
                    if cur.next is None:
                        self._tail = prev
                self._size -= 1
                return
            prev, cur = cur, cur.next
        raise ValueError(f"{value!r} not in LinkedList")

    def clear(self) -> None:
        self._head = self._tail = None
        self._size = 0

    def find(self, value: T) -> int:
        """Return index of first value or -1 if not found."""
        idx = 0
        cur = self._head
        while cur is not None:
            if cur.value == value:
                return idx
            cur = cur.next
            idx += 1
        return -1

    def to_list(self) -> list[T]:
        return list(self)

    def reverse(self) -> None:
        """In-place reverse the list."""
        prev: Optional[Node[T]] = None
        cur = self._head
        self._tail = self._head
        while cur is not None:
            nxt = cur.next
            cur.next = prev
            prev, cur = cur, nxt
        self._head = prev

