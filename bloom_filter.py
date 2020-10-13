"""
Bloom filter Python example
===========================
This is a toy implementation of a Bloom filter for educational purposes.

"""

import functools
import hashlib
import math


class BloomFilter:
    """Bloom filter implementation."""

    def __init__(self, m, k):
        self._m = m
        self._k = k
        self._bits = [False] * m
        self._hash_fns = [functools.partial(self._Hash, i) for i in range(k)]

    def _Hash(self, seed, x):
        """This method with different seed values make up the k hash functions."""
        h = hashlib.md5()
        h.update(b'%d' % seed)
        h.update(b'%d' % x)
        return int.from_bytes(h.digest(), signed=False, byteorder='big') % self._m

    def Add(self, x):
        """Add an element to the set."""
        for f in self._hash_fns:
            self._bits[f(x)] = True

    def Has(self, x):
        """Query the set for an element, may return false positives."""
        for f in self._hash_fns:
            if not self._bits[f(x)]:
                return False
        return True


if __name__ == '__main__':
    bf = BloomFilter(m=200, k=3)

    for x in range(20):
        bf.Add(x)

    for x in range(21, 100):
        if bf.Has(x):
            print('False positive:', x)