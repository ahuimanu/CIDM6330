# Barky Refactor 1

Barky is inspired by Dane Hillard's (https://github.com/daneah/practices-of-the-python-pro) Bark example of an application that demonstrates some basic software engineering principles such as:

Let's look at the elements in this list more carefully to guide what we'll do in this firs refactor:



* Abstraction - The ability to design for extension by separating the generic from the concrete.
* Extensibility - The ability to design for future expansion or redefinition
* Inheritance - The ability for code to evolve through extension and obscuration
* Loose Coupling and Cohesion - Code belongs together without inhibiting the ability for that code to independently evolve.
* Refactoring - Changing/Improving code structure without changing code function.
* Separation of concerns - Organizing code around broad or categorical focus.

This repository is an extension of Dane's example to also include testing.  This is all inspired by Dane's [Practices fo the Python Pro](https://www.manning.com/books/practices-of-the-python-pro) book, which I have found to be a great read.

# Layered Architecture

At a basic level, the architecture is designed with a layered strategy to include the following common/typical elements:

* **Presentation Layer** (will be a module called barky.py here)
* **Business Logic Layer** (will be a module called commands.py here)
* **Presistence Layer** (will be a module called database.py here)

We'll implement this layered archicture alongside and within the provisions of Django.

# Leveraging the Django ORM

## Persistence
If we use the Django ORM then our task is to create a model to represent the table rather than raw SQL.

So, whereas we utilize a table in the database called `bookmarks`:

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

We also create a Django model class that mirrors the SQL Schema:

```python
class Bookmark (models.Model):
    id = models.IntegerField()
    title = models.CharField(max=255)
    url = models.URLField()
    notes = models.TextField()
    date_added = models.DateField()

```

## Django REST Framework

[Quickstart](https://www.django-rest-framework.org/tutorial/quickstart/)

## Barky Refactoring Roadmap
Dane Hillard's code focused on a command-line interface, but we will systematically refactor that code, across a series of branches, to do the following:

1. Replace the custom data handling (the DatabaseManager module) with the [Django O/RM](https://docs.djangoproject.com/en/5.0/topics/db/queries/)
    1. Replace the existing DatabaseManager with a combination of the repository pattern and the Django ORM.
    1. Complete the implicit and explicit promises of the existing Data API 
2. Replace the CLI web-based REST API using the Django REST Framework
3. Improve architecture:
    1. SOLID
    2. Repository Pattern and Unit of Work (understand how the Django ORM is really doing this)
    3. Dependency injection