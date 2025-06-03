from typing import TypeVar, Generic
import numpy as np
import numpy.typing as npt


E = TypeVar("E", bound=np.generic)


class Vector(Generic[E]):
    _RESIZE_FACTOR: int = 2
    _SHIRNK_THRESHOLD: float = 0.25

    _INITIAL_ARRAY_CAPACITY: int = 100

    def __init__(self):
        self._items: npt.NDArray = np.empty(self._INITIAL_ARRAY_CAPACITY, dtype=object)
        self._size = 0

    def __repr__(self) -> str:
        return repr(self._items[: self.size].tolist())

    def __iter__(self):
        return iter(self._items[: self.size])

    def __eq__(self, other) -> bool:
        return list(self) == other

    @property
    def size(self) -> int:
        return self._size

    def to_list(self) -> list[E]:
        return self._items[: self.size].tolist()

    def _resize(self, new_capacity: int) -> None:
        resized_items = np.empty(new_capacity, dtype=object)
        resized_items[: self.size] = self._items[: self.size]
        self._items = resized_items

    def capacity(self) -> int:
        return self._items.size

    def is_empty(self) -> bool:
        return not self.size

    def at(self, index: int) -> E:
        if index < 0 or index > self.size:
            raise IndexError(
                f"Index out of range: size is {self.size}, but requested index is {index}"
            )

        return self._items[index]

    def push(self, item: E) -> None:
        if self.size + 1 > self.capacity():
            self._resize(self.capacity() * self._RESIZE_FACTOR)

        self._size += 1
        self._items[self.size - 1] = item

    def insert(self, index: int, item: E) -> None:
        if index < 0 or index > self.size:
            raise IndexError(
                f"Index out of range: size is {self.size}, but requested index is {index}"
            )

        if self.size + 1 > self.capacity():
            self._resize(self.capacity() * self._RESIZE_FACTOR)

        items_to_shift = self._items[index : self.size]
        self._items[index + 1 : self.size + 1] = items_to_shift
        self._items[index] = item
        self._size += 1

    def prepend(self, item: E) -> None:
        self.insert(0, item)

    def pop(self) -> E:
        if self.size - 1 < self.capacity() * self._SHIRNK_THRESHOLD:
            self._resize(self.capacity() // self._RESIZE_FACTOR)

        self._size -= 1

        result = self._items[self.size]
        self._items[self.size] = None
        return result

    def delete(self, index: int):
        if index < 0 or index > self.size:
            raise IndexError(
                f"Index out of range: size is {self.size}, but requested index is {index}"
            )

        if self.size - 1 < self.capacity() * self._SHIRNK_THRESHOLD:
            self._resize(self.capacity() // self._RESIZE_FACTOR)

        self._items[index : self.size] = self._items[index + 1 : self.size + 1]
        self._items[self.size + 1] = None

        self._size -= 1

    def find(self, item: E) -> int:
        for i, e in enumerate(self._items[: self.size]):
            if e == item:
                return i
        return -1

    def remove(self, item: E) -> bool:
        if self.size - 1 < self.capacity() * self._SHIRNK_THRESHOLD:
            self._resize(self.capacity() // self._RESIZE_FACTOR)

        index = self.find(item)
        self.delete(index)

        return index != -1
