# Web Architectures

Eventually, we'll figure out that many others have tackled the basics of facilitating other architectural patterns via the web.  Some approaches provide you many lego pieces to built your own and others are monolithic in nature.  Thus, we will compare and contrast:
- Microservices - FastAPI and Flask
- Monoliths - Django

## Django
We'll want to see if we can combine both the API and the Event/Message Queueing with Django.

### NEW IN 2025

It would seem that [Django-Ninja](https://django-ninja.dev/) is much more FastAPI-like and may be worth exploring.

Django-Ninja does seem straight-forward:

```bash
pip install django-ninja
```
And then, make a new project

```bash
django-admin startproject api
```

Then, within the api app

```python
from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

api = NinjaAPI()


@api.get("/add")
def add(request, a: int, b: int):
    return {"result": a + b}


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
```

Then, normal Django:

```bash
./manage.py runserver
```
Now, in the browser: `http://127.0.0.1:8000/api/add?a=1&b=2`

And result:

```json
{"result": 3}
```

You do not have to use Django-Ninja and can stick to the DRF examples from below, but it is more FastAPI-like than the DRF discussed from 2024.

### FROM 2024

- [Official Django REST Framework Tutorial - A Beginners Guide](https://learndjango.com/tutorials/official-django-rest-framework-tutorial-beginners)
- [Asynchronous Tasks With Django and Celery](https://realpython.com/asynchronous-tasks-with-django-and-celery/)
- [How to Use Celery with Django for Asynchronous and Periodic Tasks : A Comprehensive Guide](https://djangocentral.com/how-to-use-celery-with-django/)
- [How to Do Periodic Tasks in a Django REST API Using Celery and Redis? - A Beginner-Friendly Guide](https://dev.to/afrozansenjuti/how-to-do-periodic-tasks-in-a-django-app-using-celery-and-redis-a-beginner-friendly-guide-3bp3)

## Reflecting the Prior Evolutions in Django

So far, we have covered the following areas:

1. Evolution 1: Design with the UML
2. Evolution 2: Providing system access through APIs
3. Evolution 3: Persistence transactions with the Repository Pattern
4. Evolution 4: Event Driven architectures with message and task queueing.

In this evolution, we can combine these via Django:

1. Django Rest Framework for APIs
2. Django Object/Relational Mapper for Repository (not quite true, but good enough)
3. Celery and Redis integrations with Django for Event Tasking and Message Queues

Looking forward, we can use the built-in unit testing in Django to implement the last Evolution - TDD/BDD/DDD

**TDD** - to ensure that inidivual units of function work
**BDD** - to ensure that a set of succcess critiera drive tests
**DDD** - to ensure that the language of validation is infused with Domain-Specific concepts that may also involve a Domain-Specific Language

### Components

- DRF is a key ingredient: [DRF QuickStart](framework)
- Celery and Redis for task and message management
- Django O/RM for repository

The code in its current state focuses solely on Django Rest Framework.

Resource: https://realpython.com/asynchronous-tasks-with-django-and-celery/

Here we focus on three main things:

1. ***Producer***: Django app
2. ***Message Broker***: Redis server
3. ***Consumer***: Celery app

### Windows Start Worker (should work on *nux too)

***NOTE***: it is VITALLY important that you limit the number of concurrent workers! See [Workers Guide for Celery](https://docs.celeryq.dev/en/stable/userguide/workers.html)

windows multi-thread approach
`celery -A tasks worker -l INFO --concurrency=2`

windows single thread approach
`celery -A tasks worker -l INFO --pool=solo`

windows with greenlets
`celery -A tasks worker -l INFO --pool=gevent --concurrency=2`

### Windows Stop Worker (should work on *nux too)

find celery process
`ps -Name celery`

stop/kill celery process
`kill -Name celery`

The documentation gives the best reference for Linux/Mac: https://docs.celeryq.dev/en/v5.4.0/userguide/workers.html#stopping-the-worker

We need to start the Celery worker in Django in a separate terminal instance. 

Here is an example for this repository:

`celery -A tasks worker -l INFO --pool=gevent --concurrency=2`

`python -m celery -A bookapi worker -l INFO --pool=gevent --concurrency=2`

## Remeber Redis

With Docker Desktop Installed: `docker pull redis`

And then, run redis: `docker run -it --rm --name redis -p 6379:6379 redis:latest`

Docker Desktop must be running when these commands executed.

### Redis on Mac Step by Step

https://becomegeeks.com/blog/a-step-by-step-guide-on-how-to-install-redis-on-macos/

### Remote Redis connection using cli

From the Redis documentation: https://redis.io/docs/latest/develop/tools/cli/

`redis-cli -u redis://[username]:[password]@[host][port]/[db-number]`

`redis-cli --tls -u redis://LJenkins:p%40ssw0rd@redis-16379.hosted.com:16379/0 PING`

# Why Even Use Celery and Redis?

credit: [How Can You Leverage Celery for Your Django App?](https://realpython.com/asynchronous-tasks-with-django-and-celery/#how-can-you-leverage-celery-for-your-django-app)

We use celery when separate, and potentially long-running, tasks should not disrupt the web/api serving functions of your applicaton. Typical web development challenges are addressed by using Celery as a distributed event/task/message queue. Here are some examples

- Sending emails
- Image processing
- Text processing: Particularly translating or LLM/GPT translation and natural language processing.
- API calls: It is extremely common to incorporate other APIs to make your app run.
- Data analysis: Real-time or transactional analytics.
- Machine learning model runs: see LLM/GPT above.
- Payment calls
- Report generation