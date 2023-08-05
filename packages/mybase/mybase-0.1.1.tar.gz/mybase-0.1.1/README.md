
# `mybase` [![Build Status](https://travis-ci.com/grimen/python-mybase.svg?branch=master)](https://travis-ci.com/grimen/python-mybase) [![PyPI version](https://badge.fury.io/py/mybase.svg)](https://badge.fury.io/py/mybase) [![Coverage Status](https://codecov.io/gh/grimen/python-mybase/branch/master/graph/badge.svg)](https://codecov.io/gh/grimen/python-mybase)

*My friendly library base class - for Python.*

## Introduction

One in general tend to need a library specific base class, but creating one for every new library with some common logger customization means redundant work every time. This library base class right now don't do much now beside setting up a default logger, but keeps library code a bit cleaner.

**NOTE:** Possibly should support being used as a mixin (e.g. `@mybase.mixin`) optionally, but not yet implemented.


## Install

Install using **pip**:

```sh
$ pip install mybase
```


## Use

Very basic **[example](https://github.com/grimen/python-mybase/tree/master/examples/basic.py)**:

```python
from mybase import Base

class Foo(Base):

    def hello():
        self.logger.log('hello from instance: `{0}`'.format(self))

foo = Foo()

# logs using default logger - with colors unless disabled via `COLORS` / `LOGGER_COLORS` env variables
foo.hello()
foo.logger.log('hello world 1')

print(foo.name)
print(repr(foo))
print(str(foo))

import logging

foo2 = Foo(logger = logging.get_logger('custom'))

# logs using custom logger
foo.hello()
foo.logger.log('hello world 2')

foo3 = Foo(logger = False)

# logs nothing
foo.hello()
foo.logger.log('hello world 3')

```


## Test

Clone down source code:

```sh
$ make install
```

Run **colorful tests**, with only native environment (dependency sandboxing up to you):

```sh
$ make test
```

Run **less colorful tests**, with **multi-environment** (using **tox**):

```sh
$ make test-tox
```


## Related

- [**`mybad`**](https://github.com/grimen/python-mybad) - *"My error base class - for Python"*


## About

This project was mainly initiated - in lack of solid existing alternatives - to be used at our work at **[Markable.ai](https://markable.ai)** to have common code conventions between various programming environments where **Python** (research, CV, AI) is heavily used.


## License

Released under the MIT license.
