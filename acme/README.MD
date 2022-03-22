# Acme Crew Scheduler

Credit to Ed Williams for formulae available at his [Aviation Formulary](https://edwilliams.org/avform147.htm)

## Simple Domain Model

![Acme Crew Scheduling](https://i.imgur.com/Axqkd0O.png)

### Dependencies

* [Python-Metar](https://github.com/python-metar/python-metar)
* [Mivek METAR TAF Parser](https://github.com/mivek/python-metar-taf-parser)
* [NOAA - ADDS - TDS](https://aviationweather.gov/dataserver) - NOAA Text Data Server for current observations
* [NOAA - ADDS - API Web Serivce](https://www.weather.gov/documentation/services-web-api)

### Key Python Language Features Demonstrated
* [dataclass](https://docs.python.org/3/library/dataclasses.html#module-dataclasses) - Described in [PEP557 - Data Classes](https://peps.python.org/pep-0557/)
* [abc](https://docs.python.org/3/library/abc.html) - A key facility for the implementation of the Object-Oriented Programming Paradigm (and many design/engineering/architectural patterns).
    * Described further in [PEP 3119 – Introducing Abstract Base Classes](https://peps.python.org/pep-3119/)

### Python Development Utilities and Packages
* [pre-commit](https://pre-commit.com/) - A framework for managing and maintaining multi-language pre-commit hooks
* [black](https://github.com/psf/black) - for [PEP8](https://peps.python.org/pep-0008/)-compliant formatting
* [isort](https://pycqa.github.io/isort/index.html) - isort is a Python utility / library to sort imports alphabetically, and automatically separated into sections and by type.
* [TOML files](https://peps.python.org/pep-0518/)
    * [Example TOML File](https://martin-thoma.com/pyproject-toml/)
* [requests](https://docs.python-requests.org/en/latest/) - Requests is an HTTP library for Python that  allows you to send HTTP/1.1 requests.

## Strongly Recommended Resources

* [Python Basics](https://pythonbasics.org/) - Outstanding synopsis of many of the Python language facilities used here.

### Pytest Notes

* [Specifying which tests to run](https://docs.pytest.org/en/7.0.x/how-to/usage.html) - `pytest -k "test_knots_to_kph" -v`
