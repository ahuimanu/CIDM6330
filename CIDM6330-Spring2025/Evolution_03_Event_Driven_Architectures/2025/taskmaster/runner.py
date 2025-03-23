from tasks import add

# app = Celery("tasks", broker="redis://localhost:6379/0")
if __name__ == "__main__":
    result = add.delay(5, 5)
    print(
        f"Task {result} has been sent: READY? {result.ready()} STATUS: {result.status}"
    )
    print(result.get())