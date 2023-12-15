import time
import pytest
from src.thread import threaded, exceptions


# >>>>>>>>>> Dummy Functions <<<<<<<<<< #
def _dummy_target_raiseToPower(x: float, power: float, delay: float = 0):
  time.sleep(delay)
  return x**power

def _dummy_raiseException(x: Exception, delay: float = 0):
  time.sleep(delay)
  raise x

def _dummy_iterative(itemCount: int, pTime: float = 0.1, delay: float = 0):
  time.sleep(delay)
  for i in range(itemCount):
    time.sleep(pTime)




# >>>>>>>>>> General Use <<<<<<<<<< #
def test_creationNoParam():
  @threaded
  def _run(*args):
    return _dummy_target_raiseToPower(*args)
  
  x = _run(2, 2)
  assert x.get_return_value() == 4

def test_creationEmptyParam():
  @threaded()
  def _run(*args):
    return _dummy_target_raiseToPower(*args)
  
  x = _run(2, 2)
  assert x.get_return_value() == 4

def test_creationWithParam():
  @threaded(daemon = True)
  def _run(*args):
    return _dummy_target_raiseToPower(*args)
  
  x = _run(2, 2)
  assert x.daemon
  assert x.get_return_value() == 4

def test_argJoin():
  @threaded(daemon = True, args = (1, 2, 3))
  def _run(*args):
    return args
  
  x = _run(8, 9)
  assert x.get_return_value() == (1, 2, 3, 8, 9)
