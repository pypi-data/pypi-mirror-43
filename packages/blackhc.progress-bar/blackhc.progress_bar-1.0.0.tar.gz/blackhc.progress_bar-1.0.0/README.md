# Progress Bar

[![Build Status](https://travis-ci.com/BlackHC/progress_bar.svg?branch=master)](https://travis-ci.com/BlackHC/progress_bar) [![codecov](https://codecov.io/gh/BlackHC/progress_bar/branch/master/graph/badge.svg)](https://codecov.io/gh/BlackHC/progress_bar) [![PyPI](https://img.shields.io/badge/PyPI-progress_bar-blue.svg)](https://pypi.python.org/pypi/progress_bar/)

A progress bar that is either using TQDM for nice outputs internally, or a log-friendly replacement that works well for piping into files.

## Example

```python
from blackhc.progress_bar import with_progress_bar, use_tqdm

use_tqdm = False

for _ in with_progress_bar(range(100000)):
    pass
```

Without `use_tqdm = False`, the package will decide whether to use tqdm or not based on whether output is attached to a terminal or not.

## Installation

To install using pip, use:

```
pip install blackhc.progress_bar
```

To run the tests, use:

```
python setup.py test
```
