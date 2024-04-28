import typing
import pytest
from thread import ConcurrentProcessing


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
    def __init__(self) -> None:
        ...


class DummyUnlikeSequence2:
    def __init__(self) -> None:
        ...

    def __str__(self) -> str:
        return 'invalid'


# >>>>>>>>>> Length Only <<<<<<<<<< #
def test_LO_init() -> None:
    ConcurrentProcessing(
        function=lambda x: x,
        dataset=DummyLengthOnly(10),
        _get_value=lambda *_: _,
    )


def test_LO_init_missingGetValueError_nothing() -> None:
    with pytest.raises(TypeError):
        ConcurrentProcessing(
            function=lambda x: x,
            dataset=DummyLengthOnly(10),  # type: ignore
        )


def test_LO_init_missingGetValueError_lengthNum() -> None:
    with pytest.raises(TypeError):
        ConcurrentProcessing(
            function=lambda x: x,
            dataset=DummyLengthOnly(10),  # type: ignore
            _length=1,
        )


def test_LO_init_missingGetValueError_lengthFunc() -> None:
    with pytest.raises(TypeError):
        ConcurrentProcessing(
            function=lambda x: x,
            dataset=DummyLengthOnly(10),  # type: ignore
            _length=lambda _: 1,
        )


def test_LO_init_invalidLengthValueError_negative() -> None:
    with pytest.raises(ValueError):
        ConcurrentProcessing(
            function=lambda x: x,
            dataset=DummyLengthOnly(-10),
            _get_value=lambda *_: _,
        )


def test_LO_init_invalidLengthValueError_zero() -> None:
    with pytest.raises(ValueError):
        ConcurrentProcessing(
            function=lambda x: x,
            dataset=DummyLengthOnly(0),
            _get_value=lambda *_: _,
        )


def test_LO_init_nonIntLengthError_numLike() -> None:
    with pytest.raises(TypeError):
        ConcurrentProcessing(
            function=lambda x: x,
            dataset=DummyLengthOnly(10.5),
            _get_value=lambda *_: _,
        )


def test_LO_init_nonIntLengthError() -> None:
    with pytest.raises(TypeError):
        ConcurrentProcessing(
            function=lambda x: x,
            dataset=DummyLengthOnly('10'),
            _get_value=lambda *_: _,
        )


def test_LO_enforceTypes() -> None:
    def validate(x, i):
        assert isinstance(x, DummyLengthOnly)
        assert isinstance(i, int)

    process = ConcurrentProcessing(
        function=lambda x: x,
        dataset=DummyLengthOnly(10),
        _get_value=validate,
    )
    process.start()
    process.join()


def test_LO_len() -> None:
    process = ConcurrentProcessing(
        function=lambda x: x,
        dataset=DummyLengthOnly(10),
        _get_value=lambda *_: _,
    )
    assert process._length == 10


# >>>>>>>>>> Get Only <<<<<<<<<< #
def test_GO_init_int() -> None:
    ConcurrentProcessing(
        function=lambda x: x, dataset=DummyGetOnly([1, 2, 3]), _length=3
    )


def test_GO_init_func() -> None:
    ConcurrentProcessing(
        function=lambda x: x, dataset=DummyGetOnly([1, 2, 3]), _length=lambda _: 3
    )


def test_GO_init_missingLengthError() -> None:
    with pytest.raises(TypeError):
        ConcurrentProcessing(
            function=lambda x: x,
            dataset=DummyGetOnly([1, 2, 3]),  # type: ignore
        )


def test_GO_init_nonIntLengthError_strLike() -> None:
    with pytest.raises(TypeError):
        ConcurrentProcessing(
            function=lambda x: x,
            dataset=DummyGetOnly([1, 2, 3]),
            _length='10',  # type: ignore
        )


def test_GO_init_nonIntLengthError_numLike() -> None:
    with pytest.raises(TypeError):
        ConcurrentProcessing(
            function=lambda x: x,
            dataset=DummyGetOnly([1, 2, 3]),
            _length=10.5,  # type: ignore
        )


def test_GO_init_nonIntLengthError_negative() -> None:
    with pytest.raises(ValueError):
        ConcurrentProcessing(
            function=lambda x: x,
            dataset=DummyGetOnly([1, 2, 3]),
            _length=-10,  # type: ignore
        )


def test_GO_enforceTypes() -> None:
    def validate(x, i):
        assert isinstance(x, DummyGetOnly)
        assert isinstance(i, int)

    process = ConcurrentProcessing(
        function=lambda x: x,
        dataset=DummyGetOnly([1, 2, 3]),
        _length=3,
        _get_value=validate,
    )
    process.start()
    process.join()


def test_GO_len() -> None:
    process = ConcurrentProcessing(
        function=lambda x: x,
        dataset=DummyGetOnly([1, 2, 3]),
        _length=3,
        _get_value=lambda *_: _,
    )
    assert process._length == 3


def test_GO_get() -> None:
    def get(*_):
        return _

    process = ConcurrentProcessing(
        function=lambda x: x,
        dataset=DummyGetOnly([1, 2, 3]),
        _length=3,
        _get_value=get,
    )
    assert process._retrieve_value == get


# >>>>>>>> Sequence Like <<<<<<<< #
def test_SO_init() -> None:
    ConcurrentProcessing(
        function=lambda x: x,
        dataset=DummySequenceLike(10, list(range(10))),
    )


def test_SO_init_list() -> None:
    ConcurrentProcessing(
        function=lambda x: x,
        dataset=[1, 2, 3],
    )


def test_SO_init_tuple() -> None:
    ConcurrentProcessing(
        function=lambda x: x,
        dataset=(1, 2, 3),
    )


def test_SO_init_set() -> None:
    with pytest.raises(TypeError):
        ConcurrentProcessing(
            function=lambda x: x,
            dataset=set([1, 2, 3]),  # type: ignore
        )


def test_SO_init_dict() -> None:
    ConcurrentProcessing(
        function=lambda x: x,
        dataset={1: 1, 2: 2, 3: 3},  # type: ignore
    )


def test_SO_init_str() -> None:
    ConcurrentProcessing(
        function=lambda x: x,
        dataset='123',
    )


def test_SO_init_withLength() -> None:
    ConcurrentProcessing(
        function=lambda x: x,
        dataset=DummySequenceLike(10, list(range(10))),
        _length=10,
    )


def test_SO_init_withGet() -> None:
    ConcurrentProcessing(
        function=lambda x: x,
        dataset=DummySequenceLike(10, list(range(10))),
        _get_value=lambda *_: _,
    )


def test_SO_init_withLengthAndGet() -> None:
    ConcurrentProcessing(
        function=lambda x: x,
        dataset=DummySequenceLike(10, list(range(10))),
        _length=10,
        _get_value=lambda *_: _,
    )


def test_SO_len() -> None:
    process = ConcurrentProcessing(
        function=lambda x: x,
        dataset=DummySequenceLike(10, list(range(10))),
    )
    assert process._length == 10


def test_SO_enforceTypes() -> None:
    def validate(x, i):
        assert isinstance(x, DummySequenceLike)
        assert isinstance(i, int)

    process = ConcurrentProcessing(
        function=lambda x: x,
        dataset=DummySequenceLike(10, list(range(10))),
        _get_value=validate,
    )
    process.start()
    process.join()


# >>>>>>>>>> Unlike Sequence <<<<<<<<<< #
def test_UO_init_clean() -> None:
    with pytest.raises(TypeError):
        ConcurrentProcessing(
            function=lambda x: x,
            dataset=DummyUnlikeSequence1(),  # type: ignore
        )


def test_UO_init_withOtherMethods() -> None:
    with pytest.raises(TypeError):
        ConcurrentProcessing(
            function=lambda x: x,
            dataset=DummyUnlikeSequence2(),  # type: ignore
        )


def test_UO_init_onlyLength() -> None:
    with pytest.raises(TypeError):
        ConcurrentProcessing(
            function=lambda x: x,
            dataset=DummyUnlikeSequence1(),  # type: ignore
            _length=10,
        )


def test_UO_init_onlyGet() -> None:
    with pytest.raises(TypeError):
        ConcurrentProcessing(
            function=lambda x: x,
            dataset=DummyUnlikeSequence1(),  # type: ignore
            _get_value=lambda *_: _,
        )


def test_UO_init_onlyLengthAndGet() -> None:
    ConcurrentProcessing(
        function=lambda x: x,
        dataset=DummyUnlikeSequence1(),  # type: ignore
        _length=10,
        _get_value=lambda *_: _,
    )


def test_UO_lengthInt() -> None:
    process = ConcurrentProcessing(
        function=lambda x: x,
        dataset=DummyUnlikeSequence1(),
        _length=10,
        _get_value=lambda *_: _,
    )
    assert process._length == 10


def test_UO_lengthFunc() -> None:
    process = ConcurrentProcessing(
        function=lambda x: x,
        dataset=DummyUnlikeSequence1(),
        _length=lambda _: 10,
        _get_value=lambda *_: _,
    )
    assert process._length == 10


def test_UO_enforceTypes() -> None:
    def validate(x, i):
        assert isinstance(x, DummyUnlikeSequence1)
        assert isinstance(i, int)

    process = ConcurrentProcessing(
        function=lambda x: x,
        dataset=DummyUnlikeSequence1(),
        _length=10,
        _get_value=validate,
    )
    process.start()
    process.join()
