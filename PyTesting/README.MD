# Exploring PyTest for Testing Exercises

Various demonstrations and examples of testing will be placed here.

## Install PyTest

First, always make sure your virtual environment is activated.

`pip install pytest`

We can use a coverage plugin that works with pytest.

`pip install pytest-cov`

We will also use a conftest.py file should we wish to share fixtures across tests. This file also does double duty by making packages and modules more visible to your tests without "installing" those packages.

[conftest.py](https://docs.pytest.org/en/7.0.x/reference/fixtures.html?highlight=conftest#conftest-py-sharing-fixtures-across-multiple-files)

## Consider installing black

This package is useful for code formatting management.

`pip install -U black`

Run black from the root of your project:

`python -m black .`

## Data Structures

The example will explore two common data structures:
* [Stack](https://en.wikipedia.org/wiki/Stack_%28abstract_data_type%29)
* [Queue](https://en.wikipedia.org/wiki/Queue_(abstract_data_type))

The objective is to use [Pytest](https://docs.pytest.org/en/7.0.x/) to test their implementations.

## Running Pytest

We run pytest thusly: `python -m pytest`

Getting a coverage report: `python -m pytest -v --cov`