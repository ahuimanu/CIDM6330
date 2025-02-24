from fastapi import FastAPI

"""
We can use FastAPI to create a basic API

assumes that the following packages have been installed useing pip:
1. pip install fastapi
2. pip install uvicorn

We can use the built-in fastapi command run the API, but we'll need an additional package installation:
1. pip install "fastapi[standard]"

Altnatively, you we can use fastapi diectly from the command line:
1. uvicorn main:app --reload

"""
app = FastAPI()


@app.get("/api/greet")
def greet():
    return {"message": "Ahoy, World!"}


@app.get("/api/greet/{name}")
def greet(name: str):
    return {"message": f"Ahoy, {name}!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
