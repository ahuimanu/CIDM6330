from django.test import TestCase
from django.urls import reverse_lazy
from ninja.testing import TestClient
from django.test import Client

from .api import router as list_router

# built-in Django Test Client
class ViewTest(TestCase):
    def setUp(self):
        # This method is called before each test
        # arrange
        self.client = Client()

    def test_index(self):
        # act
        path = reverse_lazy("apilist:index")
        response = self.client.get(path)
        # assert
        assert response.status_code == 200, "API is not reachable"
        assert response.json() == {
            "message": "Welcome to the Travel Management API"
        }, "Unexpected response message"

    def test_xyz(self):
        # act
        response = self.client.get("/api/cities/v1/")
        # assert
        assert response.status_code == 200, "API is not reachable"
        assert response.json() == {
            "message": "Welcome to the Travel Management API"
        }, "Unexpected response message"

    def test_hello(self):
        # act
        response = self.client.get("/api/v1/hello/")
        # assert
        assert response.status_code == 200, "API is not reachable"
        assert response.json() == {
            "message": "Hello, World!"
        }, "Unexpected response message"

# Create your tests here.
# built-in DjangoNinja Test Client
class BasicTest(TestCase):

    def setUp(self):
        # This method is called before each test
        # arrange
        self.client = TestClient(list_router)

    def test_basic(self):

        # act
        path = reverse_lazy("api-1.0.0:welcome")
        print(f"{path} - YO BRO LOOK AT TURTLE GO")
        self.client.get("/api/cities/v1/")
        response = self.client.get(path)
        # assert
        assert response.status_code == 200, "API is not reachable"
        assert response.json() == {
            "message": "Welcome to the Travel Management API"
        }, "Unexpected response message"

    def test_hello(self):
        # act
        path = reverse_lazy("api-1.0.0:hello")
        response = self.client.get(path)
        # assert
        assert response.status_code == 200, "API is not reachable"
        assert response.json() == {
            "message": "Hello, World!"
        }, "Unexpected response message"
