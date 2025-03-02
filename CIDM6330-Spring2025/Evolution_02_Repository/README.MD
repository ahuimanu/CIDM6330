# The repository pattern
Best practices for abstracting your datastores.

Notes:
1. can we abstract the way of querying and modifying data without knowing the implementation details?
2. Let's try with two very simple examples: csv and sqlite.

## Redbird to the Rescue
We can demonstrate most aspects of the [Repository Pattern](https://pybit.es/articles/repository-pattern-in-python/) and [Unit of Work](https://red-bird.readthedocs.io/en/stable/index.html?highlight=unit%20work#unit-of-work) using [Redbird].

To do this, we'll want: 
- Our simple simple FastAPI example
- A Pydantic model
- Installation of Redbird

## Extending from API

Recall that our API's job was to CRUD on at least ONE model.

## Repository Types

Types of Repositories we'll create:

1. In-memory
2. CSV-based
3. SQLite-based

Our objective is to have our API call data from the repository. 

### 2024 Version

Below are steps of using the outdated `redbird` repository package, which does not appear to be consistently maintained.

So, let's do some steps here:

1. Ensure you have a virtual environment (`python -m venv .venv`) and, if you do, activate it:
    1. Unix/Linux/Mac: `. ./.venv/bin/activate`
    2. Windows with Git-Bash: `. ./.venv/Scripts/activate`
2. Install Redbid: `pip install redbird`
3. [Do tutorial](https://red-bird.readthedocs.io/en/stable/getting_started.html)

***NOTE***: Redbird hasn't had a new release since early 2023 and Pydantic has moved to V2, so I downgraded the version of Pydantic in this example.  FastAPI uses pydantic.

I have demonstrated an in-memory version and a CSV version, progress to these from using the documentation:
1. [JSON Repository using RedBird](https://red-bird.readthedocs.io/en/stable/repos/json_dir.html)
2. [SQLite (RedBird SQLExpressions) Repository using RedBird](https://red-bird.readthedocs.io/en/stable/repos/sql/sql-expr.html)

### 2025 Version

For the 2025 version, I'll follow the original article from Pybites and use sqlmodel for OR/M duties as it interoperates with Pydantic models.

1. Ensure you have a virtual environment (`python -m venv .venv`) and, if you do, activate it:
    1. Unix/Linux/Mac: `. ./.venv/bin/activate`
    2. Windows with Git-Bash: `. ./.venv/Scripts/activate`
2. Install [SQLModel](https://sqlmodel.tiangolo.com/): `pip install sqlmodel`
3. [Read/Follow Pybites article](https://pybit.es/articles/repository-pattern-in-python/)


## Next Steps

1. We'll want to wire up [FastAPI calls to these repo methods](https://red-bird.readthedocs.io/en/stable/examples/crud_api.html)
2. We'll want to convert to using a proper [SQL ORM Repository](https://red-bird.readthedocs.io/en/stable/repos/sql/sql-orm.html)