import typing
from src.thread import ParallelProcessing


class DummyLengthOnly:
    length: typing.Any

    def __init__(self, length: typing.Any):
        self.length = length

    def __len__(self) -> typing.Any:
        return self.length


class DummyGetOnly:
    dataset: list

    def __init__(self, dataset: list):
        self.dataset = dataset

    def __getitem__(self, i: int) -> typing.Any:
        return self.dataset[i]


class DummySequenceLike(DummyLengthOnly, DummyGetOnly):
    length: typing.Any
    dataset: list

    def __init__(self, length: typing.Any, dataset: list):
        DummyLengthOnly.__init__(self, length)
        DummyGetOnly.__init__(self, dataset)
