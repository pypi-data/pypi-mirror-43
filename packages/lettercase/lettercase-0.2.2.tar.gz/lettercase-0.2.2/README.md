# Lettercase
[![CircleCI](https://circleci.com/gh/gieseladev/lettercase.svg?style=svg)](https://circleci.com/gh/gieseladev/lettercase)
[![PyPI](https://img.shields.io/pypi/v/lettercase.svg)](https://pypi.org/project/lettercase)

A Python library for detecting and converting between various letter
cases.

Supported cases:
- snake_case
- SCREAMING_SNAKE_CASE
- Darwin_Case
- dromedaryCase
- PascalCase

## Installation
Using pip
```shell
pip install lettercase
```

## Usage
The basic usage of the library is pretty straight-forward.

To simply convert a string to another case:
```pydocstring
>>> import lettercase

>>> lettercase.convert_to("helloWorld", "snake")
hello_world
```

To detect the case, use the `detect_case` function
which returns a set of all possible cases for the given
string.
```pydocstring
>>> import lettercase

>>> lettercase.detect_case("helloWorld")
{LetterCase.DROMEDARY}
```

By default the function only checks as much of the string
as is necessary to get a unique match, however, if you need
to make sure that the letter case is correct for the entire string,
you can pass `fast_return=False`.