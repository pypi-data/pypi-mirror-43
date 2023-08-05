Stacksplit
==========

A simple Python library to generate all combinations of possible splits for a stack with given height.

## Introduction
This library aims to generate all possible combinations to split a given integer `num` into a given number of parts; the sum of all those parts shall again be the given `num`.

We wrote this simple library out of lack of such functionality needed in a lecture of our Computer Science BSc-Degree.
The original use case was to calculate and solve extended versions of the NIM-game, where towers of coins could also be splitted into multpile smaller towers.

## Usage
Be sure to have stacksplit installed.

Import stacksplit library:
```python
import stacksplit
```

The function provided is **_split_** and is implemented as a Python-generator; it takes 2 (optionally 3) arguments:
- `num`: the Integer to be split up
- `parts`: the number of parts
- `smallest`: the smallest part shall be >= the given parameter. This parameter is **optional** and defaults to 1.

```python
split(num, parts, smallest)
```

Each call returns a new tuple with a new combination with all elements summing up to `num`.

look at doc_strings and comments in init and core for help

### Examples
### Simple usage
```python
import stacksplit

for s in stacksplit.split(50, 3):
  print(s)
```
Output:
```
(1, 1, 48)
(1, 2, 47)
...
```
### More options
```python
from stacksplit import split

for i in split(50, 3, 10):
  print(i)
```
Output:
```
(10, 10, 30)
(10, 11, 29)
...
```
### Extended usecases
`smallest` can also be 0 or negative. The results will always sum up to `num`.
```python
from stacksplit import split

for i in split(5, 3, -1):
  print(i)
```
Output:
```
(-1, -1, 7)
(-1, 0, 6)
(-1, 1, 5)
...
```

## Performance
The library uses Python native generators to achieve the fast generation of results; however you have to understand that the problem itself is quite complex and the number of results will increment exponentially with higher values as parameters.

The following graphs visualize this growth of results.

Graph |Description
------|-----
![constant parts, increment num](./docs/xnum_yres_parts4_small.png) | **y-axis**: number of result <br> **x-axis**: the `num` parameter <br> `parts`: constant 4
![constant num, increment parts](./docs/xparts_yres_small.png) | **y-axis**: number of results <br> **x-axis**: the `parts` parameter <br>`num`: constant

## Installation
This library can be installed via `pip install stacksplit`.

### Arch Linux
The AUR package will be named `python-stacksplit`.

## Testing
To run the tests for stacksplit:

* install pipenv (https://pypi.org/project/pipenv/)
* clone this repository
* in this repository run `pipenv install --dev`

You may then use these:

* run normal tests: `pipenv run python setup.py test`
* run tests with coverage: `pipenv run python setup.py test --coverage`
* run tox tests: `pipenv run tox` (make sure you have interpreters for python - 3.4 to 3.7)


_Note:
It is possible to use a normal virtual environmet by installing the dev-dependencies from Pipfile by hand with pip. (For exact versions see Pipfile.lock)_


## Authors
* Micheal Oberrauch - bloor.mo@protonmail.com
* Felix Wallner - felix.wallner@protonmail.com

