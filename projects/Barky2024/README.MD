# Barky 

Barky is inspired by Dane Hillard's (https://github.com/daneah/practices-of-the-python-pro) Bark example of an application that demonstrates some basic software engineering principles such as:

* Separation of concerns
* Loose Coupling
* Inheritance
* Extensibility
* Abstraction
* Refactoring

This repository is an extension of Dane's example to also include testing.  This is all inspired by Dane's [Practices fo the Python Pro](https://www.manning.com/books/practices-of-the-python-pro) book, which I have found to be a great read.

# Layered Architecture

At a basic level, the architecture is designed with a layered strategy to include the following common/typical elements:

* **Presentation Layer** (will be a module called barky.py here)
* **Business Logic Layer** (will be a module called commands.py here)
* **Presistence Layer** (will be a module called database.py here)

# Bare Bones Approach

## Persistence
We will take a bare bones approach and connect directly to a sqlite database.

The [DB Browser for SQLite](https://sqlitebrowser.org/) tool will be useful to inspect the data and manage the database file.

The initial database wil consist of a table called `bookmarks`:

``` sql
CREATE TABLE IF NOT EXISTS bookmarks
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    notes TEXT,
    date_added TEXT NOT NULL
);
```

## Using this Example
The example requires the [requests](https://docs.python-requests.org/en/latest/index.html) python package and this dependency is indicated within the `requirements.txt` file.

So, the basic steps will be:
1. If you don't have a virtual environment to work with: `python -m venv venv` #creates a new virtual environment called `./venv`
2. Activate the virtual environment:
    1. Windows: `./venv/Scripts/activate` (or if using gitbash: `source ./venv/Scripts/activate`)
    2. Mac/*nix: `source ./venv/bin/activate`
3. install the dependencies: `pip install -r requirements.txt`
4. Run the code: `python barky.py`

You fill find that the database module handles itself, so there is nothing left to do but run the project.  We'll use Barky as an example from which we can learn more about applying architectural patterns to our work.

## Refactoring Barky
Dane Hillard's code focused on a command-line interface, but we will systematically refactor that code, across a series of branches, to do the following:

1. Replace the custom data handling (the DatabaseManager module) with the [Django O/RM](https://docs.djangoproject.com/en/5.0/topics/db/queries/)
    1. Replace the existing DatabaseManager with a combination of the repository pattern and the Django ORM.
    1. Complete the implicit and explicit promises of the existing Data API 
2. Replace the CLI web-based REST API using the Django REST Framework
3. Improve architecture:
    1. SOLID
    2. Repository Pattern and Unit of Work (understand how the Django ORM is really doing this)
    3. Dependency injection