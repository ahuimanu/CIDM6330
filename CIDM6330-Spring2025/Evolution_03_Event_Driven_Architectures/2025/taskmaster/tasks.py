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
    print(f"Multiplying {x} + {y}")    
    return x * y
