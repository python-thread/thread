from src.thread.utils import algorithm


def test_chunking_1():
  assert algorithm.chunk_split(5, 1) == [(0, 5)]


def test_chunking_2():
  assert algorithm.chunk_split(5, 2) == [(0, 3), (3, 5)]


def test_chunking_3():
  assert algorithm.chunk_split(100, 8) == [
    (0, 13),
    (13, 26),
    (26, 39),
    (39, 52),
    (52, 64),
    (64, 76),
    (76, 88),
    (88, 100),
  ]
