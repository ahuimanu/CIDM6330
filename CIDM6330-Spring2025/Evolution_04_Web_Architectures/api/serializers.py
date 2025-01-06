from .models import Author, Book, Publisher, Reader
from rest_framework import serializers


class BookSerlializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["authors", "title", "publish_date", "publisher", "isbn"]


class AuthorSerlializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["first_name", "middle_name", "last_name", "email"]


class PublisherSerlializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ["name", "address", "city", "state", "country", "postcode"]


class ReaderSerlializer(serializers.ModelSerializer):
    class Meta:
        model = Reader
        fields = ["first_name", "middle_name", "last_name", "email", "membership"]
