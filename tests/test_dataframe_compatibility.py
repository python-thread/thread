import typing
from src.thread import ParallelProcessing


class DummyLengthOnly:
    length: int

    def __init__(self, length: int):
        self.length = length

    def __len__(self) -> int:
        return self.length


class DummyGetOnly:
    dataset: list

    def __init__(self, dataset: list):
        self.dataset = dataset

    def __getitem__(self, i: int) -> typing.Any:
        return self.dataset[i]


class DummyNonSequence(DummyLengthOnly, DummyGetOnly):
    length: int
    dataset: list

    def __init__(self, length: int, dataset: list):
        DummyLengthOnly.__init__(self, length)
        DummyGetOnly.__init__(self, dataset)
