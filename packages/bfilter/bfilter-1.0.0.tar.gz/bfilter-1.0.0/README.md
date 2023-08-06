# A Simple Bloom Filter for Python

[![Build Status](https://travis-ci.org/sysatom/python-bloom-filter.svg?branch=master)](https://travis-ci.org/sysatom/python-bloom-filter)

### Install

```bash
pip install PyBloomFilter
```

### Usage

```python
from bfilter.bloomfilter import BloomFilter

bf = BloomFilter(100000, 7)
for i in range(5000):
    bf.add('%s' % i)

print(bf.lookup('333'))
print(bf.lookup('100000'))
print(bf.lookup('500001'))
print(bf.lookup('510001'))
```

### Requirements

This project requires Python 3.6 or newer.

### License


You can find the license for this code in [the LICENSE file](LICENSE).
