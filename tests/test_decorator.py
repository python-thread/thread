import time
from src.thread import threaded


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
  @threaded(daemon = True)
  def _run(*args):
    return _dummy_target_raiseToPower(*args)
  
  x = _run(2, 2)
  assert x.daemon
  assert x.get_return_value() == 4

def test_threadedArgJoin():
  @threaded(daemon = True, args = (1, 2, 3))
  def _run(*args):
    return args
  
  x = _run(8, 9)
  assert x.get_return_value() == (1, 2, 3, 8, 9)
