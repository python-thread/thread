"""
This file shall host the shared algorithms

If it gets too dense, we could consider splitting it into a library import
|_ algorithm/
  |_ __init__.py
  |_ a.py
  |_ b.py
"""

from typing import List, Tuple


def chunk_split(dataset_length: int, number_of_chunks: int) -> List[Tuple[int, int]]:
  """
  Splits a dataset into balanced chunks

  If the size of the dataset is not fully divisible by the number of chunks, it is split like this
    > `[ [n+1], [n+1], [n+1], [n], [n], [n] ]`


  Parameters
  ----------
  :param dataset: This should be the dataset you want to split into chunks
  :param number_of_chunks: The should be the number of chunks it will attempt to split into


  Returns
  -------
  :returns list[list[Any]]: The split dataset

  Raises
  ------
  AssertionError: The number of chunks specified is larger than the dataset size
  """
  length = len(dataset)
  assert (
    length >= number_of_chunks
  ), 'The number of chunks specified is larger than the dataset size'

  chunk_count = length // number_of_chunks
  overflow = length % number_of_chunks

  i = 0
  split = []
  while i < length:
    chunk_length = chunk_count + int(overflow > 0)
    b = i + chunk_length

    split.append(dataset[i:b])
    overflow -= 1
    i = b

  return split
