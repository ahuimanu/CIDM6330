from fastapi import FastAPI

app = FastAPI()


@app.get("/api/greet")
def greet():
    return {"message": "Ahoy, World!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
