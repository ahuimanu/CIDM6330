# Event-Driven Architectures

Our next overall design concept is to determine how we can implement event-driven architectures

## Docker, Celery, and Redis

Eventually, we need to have a reliable execution environment for our applications where the variability and vagaries of Linux, Mac, and Windows must be "leveled" with containerization and virtualization.

[Docker](https://www.docker.com/) is the go to platform for containerization and there is ample support for running [Python with Docker](https://realpython.com/docker-continuous-integration/).

In order to learn about message-driven architectures, this evolution will see us working with an event bus and and message queue where the implementation tools we will rely are are:

- [Celery](https://docs.celeryq.dev/en/stable/index.html) for event-driven task queueing
- [Redis](https://redis.io/) to act as a message bus/broker
- [Docker](https://www.docker.com/) to serve as a Virtualized Computing Image container so that the support tools run reliably

## Event-driven architectures
Celery is a distributed task queue that facilitates an event-driven, message/task queuing architecture. In such an architecture, clients of the system raise events which then causes a task to be created and sent to a central message queue to be processed asynchronously available task workers workers. Simply put, an event-driven architecture facilitates asynchronous and parallel task execution. 

## Using Celery

We will use Celery, which is a task queue that emphasized real-time task processing and task scheduling. Celery facilitates the following common concepts:

- **Message Broker** – This is a message queue used to exchange messages between clients and workers. We will use Redis with Celery to acocmplish this.
- **Result Store** – A store for task state and results.
- **Workers** – Processes that read tasks from the broker and execute them.
- **Beat** – Scheduler that enqueues periodic tasks to be executed at prescribed intervals.


## Install Docker Desktop, Install and Run Redis

[Download Docker Desktop](https://docs.docker.com/desktop/) and follow the overview and setup steps listed at the website.

Once installed, execute this command from your terminal to download and install `redis` to be run on Docker Desktop. This is absolutely necessary for Windows folks and ideal for all else.

`docker pull redis`

This will grab a docker image for redis and install it on Docker Desktop.

Next, we can redis within docker with this command:

`docker run -it --rm --name redis -p 6379:6379 redis:latest`

## Install Celery and the Redis Python Packages

With a virtual environment active, not to be confused with the docker container above, install celery:

1. Step 0 (review) - create virtual environment: `python -m venv .venv`
2. Step 1 (review) - activate virtual environment: (on Windows) `. ./.venv/Scripts/activate`; (all others) `. ./.venv/bin/activate`
3. Step 2 - install celery and redis: `pip install celery redis`

## Create and Configure Celery Application

The simplest celery configuration and task setup is seen below:

```python
from celery import Celery

BROKER_URL = "redis://localhost:6379/0"
BACKEND_URL = "redis://localhost:6379/1"

app = Celery(
    "tasks",
    broker=BROKER_URL,
    backend=BACKEND_URL,    
)

@app.task
def add(x, y):
    print(f"Adding {x} + {y}")
    return x + y


@app.task
def multiply(x, y):
    return x * y
```

Note that the database number in the redis URL for the broker must be different from the backend.


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

## Results
This example, which closely follows the [Celery User Guide](https://docs.celeryq.dev/en/v5.4.0/userguide/application.html), simply shows that the message broker and task results queue can be configured using Redis and Celery.

## Your Job
Your job would be to bring some simple transaction in from your context and elaborate from the basic example.