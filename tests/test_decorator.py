import time
from src.thread import threaded, processor


# >>>>>>>>>> Dummy Functions <<<<<<<<<< #
def _dummy_target_raiseToPower(x: float, power: float, delay: float = 0):
    time.sleep(delay)
    return x**power


# >>>>>>>>>> Threaded <<<<<<<<<< #
def test_threadedCreationNoParam():
    @threaded
    def _run(*args):
        return _dummy_target_raiseToPower(*args)

    x = _run(2, 2)
    assert x.get_return_value() == 4


def test_threadedCreationEmptyParam():
    @threaded()
    def _run(*args):
        return _dummy_target_raiseToPower(*args)

    x = _run(2, 2)
    assert x.get_return_value() == 4


def test_threadedCreationWithParam():
    @threaded(daemon=True)
    def _run(*args):
        return _dummy_target_raiseToPower(*args)

    x = _run(2, 2)
    assert x.daemon
    assert x.get_return_value() == 4


def test_threadedArgJoin():
    @threaded(daemon=True, args=(1, 2, 3))
    def _run(*args):
        return args

    x = _run(8, 9)
    assert x.get_return_value() == (1, 2, 3, 8, 9)


def test_processorCreationNoParam():
    @processor
    def _run(args):
        return _dummy_target_raiseToPower(*args)

    x = _run([[2, 2]])
    assert x.get_return_values() == [4]


def test_processorCreationEmptyParam():
    @processor()
    def _run(args):
        return _dummy_target_raiseToPower(*args)

    x = _run([[2, 2]])
    assert x.get_return_values() == [4]


def test_processorCreationWithParam():
    @processor(daemon=True)
    def _run(args):
        return _dummy_target_raiseToPower(*args)

    x = _run([[2, 2]])
    assert len(x._threads) == 1
    assert x._threads[0].thread.daemon
    assert x.get_return_values() == [4]


def test_processorArgJoin():
    @processor(daemon=True, args=(1, 2, 3))
    def _run(data, *args):
        return [*args, *data]

    x = _run([[8, 9]])
    assert x.get_return_values() == [[1, 2, 3, 8, 9]]


def test_processorMultiArgJoin():
    @processor(daemon=True, args=(1, 2, 3))
    def _run(data, *args):
        return [*args, *data]

    x = _run([[8, 9], [10, 11]])
    assert x.get_return_values() == [[1, 2, 3, 8, 9], [1, 2, 3, 10, 11]]
