from ninja import NinjaAPI, Router, Schema, Field
from apilist.api import router as list_router

api = NinjaAPI()
default_router = Router()

class HelloResponseSchema(Schema):
    message: str = Field(..., description="Hello message")
    def hello(request):
        return {"message": "Hello, World!"}
    
@default_router.get("hello/", response=HelloResponseSchema, url_name="hello")
def hello(request):
    return {"message": "Hello, World!"}

api.add_router("/v1/", default_router)
api.add_router("/cities/", list_router)
