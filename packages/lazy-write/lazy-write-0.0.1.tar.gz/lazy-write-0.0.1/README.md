# lazy-write [![Build Status](https://travis-ci.com/FebruaryBreeze/lazy-write.svg?branch=master)](https://travis-ci.com/FebruaryBreeze/lazy-write) [![codecov](https://codecov.io/gh/FebruaryBreeze/lazy-write/branch/master/graph/badge.svg)](https://codecov.io/gh/FebruaryBreeze/lazy-write) [![PyPI version](https://badge.fury.io/py/lazy-write.svg)](https://pypi.org/project/lazy-write/)

Write to File if Need for Python

## Installation

Need Python 3.6+.

```bash
pip install lazy-write
```

## Usage

```python
import lazy_write

file_path = 'test.txt'
content = 'rain & snow'

lazy_write.write(file_path, content)  # really write
lazy_write.write(file_path, content)  # check equal and not write
```
