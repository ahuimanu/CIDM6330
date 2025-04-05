from ninja import NinjaAPI
from apilist.api import router as list_router

api = NinjaAPI()

api.add_router("/cities/", list_router)
