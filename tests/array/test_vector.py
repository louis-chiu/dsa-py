import pytest

from arrays.vector import Vector


class TestVector:
    def test_push(self):
        vector = Vector()

        vector.push(1)
        assert vector.to_list() == [1]

        vector.push(2)
        assert vector == [1, 2]

        vector.push(3)
        assert vector._items[: vector.size].tolist() == [1, 2, 3]

    def test_at(self):
        vector = Vector()
        for i in range(100):
            vector.push(i)

        assert vector.at(10) == 10
        assert vector.at(99) == 99
        with pytest.raises(IndexError):
            vector.at(-100)

    def test_insert(self):
        vector = Vector()

        with pytest.raises(IndexError):
            vector.insert(1, 1)

        with pytest.raises(IndexError):
            vector.insert(100, 1)

        with pytest.raises(IndexError):
            vector.insert(-1, 1)

        vector.insert(0, 1)
        assert vector == [1]

        vector.insert(0, 2)
        assert vector == [2, 1]

        vector.insert(0, 3)
        assert vector == [3, 2, 1]

        vector.insert(2, 5)
        assert vector == [3, 2, 5, 1]

        vector.insert(1, 5)
        assert vector == [3, 5, 2, 5, 1]

        vector.insert(0, 999)
        assert vector == [999, 3, 5, 2, 5, 1]

    def test_prepend(self):
        vector = Vector()

        vector.prepend(1)
        assert vector == [1]

        vector.prepend(2)
        assert vector == [2, 1]

        vector.prepend(3)
        assert vector == [3, 2, 1]

        vector.prepend(5)
        assert vector == [5, 3, 2, 1]

        vector.prepend(5)
        assert vector == [5, 5, 3, 2, 1]

        vector.prepend(999)
        assert vector == [999, 5, 5, 3, 2, 1]

    def test_size(self):
        vector = Vector()

        vector.push(1)
        assert vector.size == 1

        vector.push(2)
        assert vector.size == 2

        vector.push(2)
        assert vector.size == 3

        for i in range(100):
            vector.push(i)
        assert vector.size == 103

    def test_pop(self):
        vector = Vector()
        for i in range(100):
            vector.push(i)
        assert vector.size == 100

        for i in range(99, -1, -1):
            assert vector.pop() == i
        assert vector.size == 0

    def test_capacity_after_resized(self):
        vector = Vector()
        assert vector.capacity() == vector._INITIAL_ARRAY_CAPACITY

        for i in range(vector.capacity() + 1):
            vector.push(i)
        assert vector.capacity() == vector._INITIAL_ARRAY_CAPACITY * 2

        while not vector.is_empty():
            current_capacity = 0
            if vector.size - 1 < vector.capacity() * vector._SHRINK_THRESHOLD:
                current_capacity = vector.capacity()

            vector.pop()

            if current_capacity != 0:
                assert current_capacity // vector._RESIZE_FACTOR == vector.capacity()

    def test_delete(self):
        vector = Vector()

        for i in range(5):
            vector.push(i)

        with pytest.raises(IndexError):
            vector.delete(777)

        with pytest.raises(IndexError):
            vector.delete(100)

        with pytest.raises(IndexError):
            vector.delete(-1)

        vector.delete(4)
        assert vector == [0, 1, 2, 3]

        vector.delete(1)
        assert vector == [0, 2, 3]

    def test_find(self):
        vector = Vector()

        for i in range(100):
            vector.push(i)

        assert vector.find(5) == 5
        assert vector.find(100) == -1
        assert vector.find(-1000) == -1
        assert vector.find(0) == 0
