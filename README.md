# postfix Lisp

This codebase was developed and tested with Python 3.7 on a MacBook Air running OS 10.15 Catalina.

## Installation

1. `git clone` this repo and `cd` into the project's top level folder

1. create a Python3 virtual environment and activate it

   `virtualenv -p python3.7 venv`

   `source venv/bin/activate`

1. install dependencies

   `pip install -r requirements.txt`

## Running locally

In the top level directory and with the virtualenv active:

`python psil.py [SOURCE]`

Sample usage:

**factorial.psil** is a source file with content:

```
(
    factorial
    (
        (x)
        (
            ((x 1 eq?) 1)
            (else (x ((x 1 -)  factorial) *))
            cond
        )
        lambda
    )
    define
)


(5 factorial)
```

Running this produces:

```
$ python psil.py factorial.psil
120
```

## Running the tests

In the top level directory and with the virtualenv active:

`python -m pytest`

Test coverage data:

`coverage run -m pytest && coverage report`

Sample output:

```
Name                 Stmts   Miss  Cover
----------------------------------------
src/interpreter.py      42      0   100%
src/parser.py           45      0   100%
----------------------------------------
TOTAL                   87      0   100%
```
