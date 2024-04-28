"""
This file shall host the shared algorithms

If it gets too dense, we could consider splitting it into a library import
|_ algorithm/
  |_ __init__.py
  |_ a.py
  |_ b.py
"""

from typing import Tuple, Generator


def chunk_split(
    dataset_length: int, number_of_chunks: int
) -> Generator[Tuple[int, int], None, None]:
    """
    Splits a dataset into balanced chunks

    If the size of the dataset is not fully divisible by the number of chunks, it is split like this
      > `[ [n+1], [n+1], [n+1], [n], [n], [n] ]`


    Parameters
    ----------
    :param dataset_length: This should be the length of the dataset you want to split into chunks
    :param number_of_chunks: The should be the number of chunks it will attempt to split into


    Returns
    -------
    :returns Generator[tuple[int, int], None, None]: The chunked dataset slices

    Raises
    ------
    AssertionError: The number of chunks specified is larger than the dataset size
    """
    assert (
        dataset_length >= number_of_chunks
    ), 'The number of chunks specified is larger than the dataset size'

    chunk_count = dataset_length // number_of_chunks
    overflow = dataset_length % number_of_chunks

    i = 0
    while i < dataset_length:
        chunk_length = chunk_count + int(overflow > 0)
        b = i + chunk_length

        yield (i, b)
        overflow -= 1
        i = b
