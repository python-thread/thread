import random
from typing import Generator

from thread.utils import algorithm


def test_type():
    assert isinstance(algorithm.chunk_split(5, 1), Generator)


def test_chunking_1():
    assert list(algorithm.chunk_split(5, 1)) == [(0, 5)]


def test_chunking_2():
    assert list(algorithm.chunk_split(5, 2)) == [(0, 3), (3, 5)]


def test_chunking_3():
    assert list(algorithm.chunk_split(100, 8)) == [
        (0, 13),
        (13, 26),
        (26, 39),
        (39, 52),
        (52, 64),
        (64, 76),
        (76, 88),
        (88, 100),
    ]


def test_chunking_dynamic():
    dataset_length = random.randint(400, int(10e6))
    thread_count = random.randint(2, 100)

    expected_chunk_length_low = dataset_length // thread_count
    expected_chunk_high = dataset_length % thread_count

    i = 0
    gen = algorithm.chunk_split(dataset_length, thread_count)
    while i < dataset_length:
        chunk_length = expected_chunk_length_low + int(expected_chunk_high > 0)
        b = i + chunk_length

        assert (
            next(gen) == (i, b)
        ), f'\nIndex: {i}\nLength: {dataset_length}\nThreads: {thread_count}\nExpected: {(i, b)}\nActual: {next(gen)}'
        expected_chunk_high -= 1
        i = b
