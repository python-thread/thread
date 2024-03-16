import typing
import pytest
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


class DummyUnlikeSequence1:
    def __init__(self) -> None: ...


class DummyUnlikeSequence2:
    def __init__(self) -> None: ...
    def __str__(self) -> str:
        return 'invalid'


# >>>>>>>>>> Length Only <<<<<<<<<< #
def test_LO_init() -> None:
    ParallelProcessing(
        function=lambda x: x,
        dataset=DummyLengthOnly(10),
        _get_value=lambda *_: _,
    )


def test_LO_init_missingGetValueError_nothing() -> None:
    with pytest.raises(TypeError):
        ParallelProcessing(
            function=lambda x: x,
            dataset=DummyLengthOnly(10),  # type: ignore
        )


def test_LO_init_missingGetValueError_lengthNum() -> None:
    with pytest.raises(TypeError):
        ParallelProcessing(
            function=lambda x: x,
            dataset=DummyLengthOnly(10),  # type: ignore
            _length=1,
        )


def test_LO_init_missingGetValueError_lengthFunc() -> None:
    with pytest.raises(TypeError):
        ParallelProcessing(
            function=lambda x: x,
            dataset=DummyLengthOnly(10),  # type: ignore
            _length=lambda _: 1,
        )


def test_LO_init_invalidLengthValueError_negative() -> None:
    with pytest.raises(ValueError):
        ParallelProcessing(
            function=lambda x: x,
            dataset=DummyLengthOnly(-10),
            _get_value=lambda *_: _,
        )


def test_LO_init_invalidLengthValueError_zero() -> None:
    with pytest.raises(ValueError):
        ParallelProcessing(
            function=lambda x: x,
            dataset=DummyLengthOnly(0),
            _get_value=lambda *_: _,
        )


def test_LO_init_nonIntLengthError_numLike() -> None:
    with pytest.raises(TypeError):
        ParallelProcessing(
            function=lambda x: x,
            dataset=DummyLengthOnly(10.5),
            _get_value=lambda *_: _,
        )


def test_LO_init_nonIntLengthError() -> None:
    with pytest.raises(TypeError):
        ParallelProcessing(
            function=lambda x: x,
            dataset=DummyLengthOnly('10'),
            _get_value=lambda *_: _,
        )


def test_LO_enforceTypes() -> None:
    def validate(x, i):
        assert isinstance(x, DummyLengthOnly)
        assert isinstance(i, int)

    process = ParallelProcessing(
        function=lambda x: x,
        dataset=DummyLengthOnly(10),
        _get_value=validate,
    )
    process.start()
    process.join()


def test_LO_len() -> None:
    process = ParallelProcessing(
        function=lambda x: x,
        dataset=DummyLengthOnly(10),
        _get_value=lambda *_: _,
    )
    assert process._length == 10


# >>>>>>>>>> Get Only <<<<<<<<<< #
def test_GO_init_int() -> None:
    ParallelProcessing(function=lambda x: x, dataset=DummyGetOnly([1, 2, 3]), _length=3)


def test_GO_init_func() -> None:
    ParallelProcessing(
        function=lambda x: x, dataset=DummyGetOnly([1, 2, 3]), _length=lambda _: 3
    )


def test_GO_init_missingLengthError() -> None:
    with pytest.raises(TypeError):
        ParallelProcessing(
            function=lambda x: x,
            dataset=DummyGetOnly([1, 2, 3]),  # type: ignore
        )


def test_GO_init_nonIntLengthError_strLike() -> None:
    with pytest.raises(TypeError):
        ParallelProcessing(
            function=lambda x: x,
            dataset=DummyGetOnly([1, 2, 3]),
            _length='10',  # type: ignore
        )


def test_GO_init_nonIntLengthError_numLike() -> None:
    with pytest.raises(TypeError):
        ParallelProcessing(
            function=lambda x: x,
            dataset=DummyGetOnly([1, 2, 3]),
            _length=10.5,  # type: ignore
        )


def test_GO_init_nonIntLengthError_negative() -> None:
    with pytest.raises(ValueError):
        ParallelProcessing(
            function=lambda x: x,
            dataset=DummyGetOnly([1, 2, 3]),
            _length=-10,  # type: ignore
        )


def test_GO_enforceTypes() -> None:
    def validate(x, i):
        assert isinstance(x, DummyGetOnly)
        assert isinstance(i, int)

    process = ParallelProcessing(
        function=lambda x: x,
        dataset=DummyGetOnly([1, 2, 3]),
        _length=3,
        _get_value=validate,
    )
    process.start()
    process.join()


def test_GO_len() -> None:
    process = ParallelProcessing(
        function=lambda x: x,
        dataset=DummyGetOnly([1, 2, 3]),
        _length=3,
        _get_value=lambda *_: _,
    )
    assert process._length == 3


def test_GO_get() -> None:
    def get(*_):
        return _

    process = ParallelProcessing(
        function=lambda x: x,
        dataset=DummyGetOnly([1, 2, 3]),
        _length=3,
        _get_value=get,
    )
    assert process._retrieve_value == get
