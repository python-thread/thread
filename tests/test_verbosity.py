import pytest
from src.thread.utils.config import Verbosity


# >>>>>>>>>> General Use <<<<<<<<<< #
def test_eqTrue():
    assert Verbosity(0) == 0
    assert Verbosity(0) == 'quiet'
    assert Verbosity(1) == 'normal'
    assert Verbosity(1) == Verbosity(1)


def test_neTrue():
    assert Verbosity(0) != 1
    assert Verbosity(0) != 'normal'
    assert Verbosity(1) != 'quiet'
    assert Verbosity(1) != Verbosity(0)


def test_ltTrue():
    assert Verbosity(0) < 1
    assert Verbosity(0) < 'normal'
    assert Verbosity(1) < 'verbose'
    assert Verbosity(1) < Verbosity(2)


def test_leTrue():
    assert Verbosity(0) <= 1
    assert Verbosity(0) <= 'normal'
    assert Verbosity(1) <= 'verbose'
    assert Verbosity(1) <= Verbosity(2)


def test_gtTrue():
    assert Verbosity(1) > 0
    assert Verbosity(1) > 'quiet'
    assert Verbosity(2) > 'normal'
    assert Verbosity(2) > Verbosity(1)


def test_geTrue():
    assert Verbosity(1) >= 0
    assert Verbosity(1) >= 'quiet'
    assert Verbosity(2) >= 'normal'
    assert Verbosity(2) >= Verbosity(1)


# >>>>>>>>>> Raising <<<<<<<<<< #
def test_ltRaise():
    with pytest.raises(ValueError):
        _ = Verbosity(0) < Exception()


def test_leRaise():
    with pytest.raises(ValueError):
        _ = Verbosity(0) <= Exception()


def test_gtRaise():
    with pytest.raises(ValueError):
        _ = Verbosity(1) > Exception()


def test_geRaise():
    with pytest.raises(ValueError):
        _ = Verbosity(1) >= Exception()
