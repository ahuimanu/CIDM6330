# CIDM6330-Fall2024
CIDM6330-Fall2024

# EVOLUTION FORMAT
1. Lectures/Dicussion from FSA/PAP
2. Review and Reflection on Previous Evolution.
2. Orientation to the purpose of the evolution
3. Q and A about Evolution

## EVOLUTION 0: UML + OOP
Please place your Diagrams in the corresponding folder.

## EVOLUTION 1: API + Models
API-Centricity (heart of system)

Exercise
Make an API for coin toss

## Three Ways

1. Flask
2. FastAPI
3. Django Rest Framework

Good reference article: [https://www.twilio.com/en-us/blog/create-api-with-python](https://www.twilio.com/en-us/blog/create-api-with-python)

## EVOLUTION 2: REPOSITORY and UoW
Clean and abstracted transactions for all state changes

## EVOLUTION 3: Event-Driven Architectures
Balancing state change requests and business rules

## EVOLUTION 4: WEB ARCHITECTURES
Leveraging the web as the application framework

## EVOLUTION 5: TDD, BDD, DDD
Validation and verificaiton

# Putting it All Together for the Final Project

- Django app that uses:
    - Django Architecture - MVC/MVT
    - Django Rest Framework for API Development
    - Django O/RM to get some of the benefits of the repository pattern
    - Django, Celery, and Redis for Message Queueing and Event Tasking
    - Django Unit Tests for TDD, BDD, DDD

Expectations:
1. Use Django for your models, views, and monolithic architecture
2. Use the Django Rest Framework for API Routing and Serliazation
3. Use Django, Celery, and Redis for message/task queuing
4. Use built-in unit testing for TDD, BDD, DDD

## Evolutions 0 and 5
- Ensure that the behaviors and structures of your app are represented by:
    - UML diagrams - class, seqeuence, activity, state, use case
    - Provide a glossary of the Ubiquitous Language that is embedded in your project [Developing the ubiquitous language](https://thedomaindrivendesign.io/developing-the-ubiquitous-language/)
    - Create testable stories and acceptance criteria, using the [BDD Gherkin syntax](https://cucumber.io/docs/gherkin/), to develop your unit tests. Read: [What is BDD?](https://cucumber.io/docs/bdd/)
    - Ensure you create tests that reflect the Gherkin Syntax feature design statements from the link above.
## Evolution 1
- Configure the [Django Rest Framework](https://www.django-rest-framework.org/) to deliver your system's API.
- Extend your basic viewsets to create at least one behavioral [extra action for routing](https://www.django-rest-framework.org/) (this will be your task handler).

## Evolution 2
- Use Django Models and DRF Serializers to provide CRUD operations for your entities

## Evolution 3
- Use Celery and Redis to create a message/event and task queue to execute asynchronous tasks in your application.

## Evolution 4
- Django serves as our comprehensive application/project framework for our entire architecture.  Bear in mind that this is a monolithic architecture as opposed to a service-based (microservices) architecture.

## Fixtures
Data that loads up my simple examples has been exported using the following Django command:

`python manage.py dumpdata api --format json --indent 4 --output ./api/fixtures/api_fixtures.json`

Use the `loaddata` django management command to import this fixture.

