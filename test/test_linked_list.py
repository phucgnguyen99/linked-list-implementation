import pytest
from linked_list import LinkedList

def test_init_and_iteration():
    ll = LinkedList([1, 2, 3])
    assert list(ll) == [1, 2, 3]
    assert len(ll) == 3

def test_append_prepend():
    ll = LinkedList()
    ll.append(2); ll.append(3)
    ll.prepend(1)
    assert list(ll) == [1, 2, 3]
    assert len(ll) == 3

@pytest.mark.parametrize("index,value,expected", [
    (0, 10, [10, 1, 2]),
    (1, 20, [1, 20, 2]),
    (2, 30, [1, 2, 30]),
    (3, 40, [1, 2, 3, 40]),
])
def test_insert_valid(index, value, expected):
    ll = LinkedList([1, 2, 3])
    ll.insert(index, value)
    assert list(ll) == expected

@pytest.mark.parametrize("index", [-1, 5])
def test_insert_invalid_index(index):
    ll = LinkedList([1, 2, 3])
    with pytest.raises(IndexError):
        ll.insert(index, 99)

def test_pop_default_and_index():
    ll = LinkedList([1, 2, 3, 4])
    assert ll.pop() == 4           # default last
    assert list(ll) == [1, 2, 3]
    assert ll.pop(0) == 1          # head
    assert list(ll) == [2, 3]
    assert ll.pop(1) == 3          # tail after previous pops
    assert list(ll) == [2]
    assert ll.pop(0) == 2
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.pop()

def test_remove_value():
    ll = LinkedList(["a", "b", "c", "b"])
    ll.remove("b")
    assert list(ll) == ["a", "c", "b"]
    ll.remove("b")
    assert list(ll) == ["a", "c"]
    with pytest.raises(ValueError):
        ll.remove("z")

def test_find_and_contains():
    ll = LinkedList([10, 20, 30])
    assert ll.find(20) == 1
    assert ll.find(99) == -1
    assert 10 in ll
    assert 99 not in ll

def test_reverse_and_clear():
    ll = LinkedList([1, 2, 3, 4])
    ll.reverse()
    assert list(ll) == [4, 3, 2, 1]
    ll.clear()
    assert list(ll) == []
    assert len(ll) == 0

def test_to_list_and_repr():
    ll = LinkedList(["x", "y"])
    assert ll.to_list() == ["x", "y"]
    r = repr(ll)
    assert "LinkedList" in r and "x" in r and "y" in r