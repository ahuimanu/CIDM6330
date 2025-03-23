from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Author, Book, Publisher, Reader
from .serializers import (
    AuthorSerlializer,
    BookSerlializer,
    PublisherSerlializer,
    ReaderSerlializer,
)
from .tasks import send_email_to_reader_members_about_book_discounts_task


# Create your views here.
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all().order_by("last_name")
    serializer_class = AuthorSerlializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by("title")
    serializer_class = BookSerlializer


class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all().order_by("name")
    serializer_class = PublisherSerlializer


class ReaderViewSet(viewsets.ModelViewSet):
    queryset = Reader.objects.all().order_by("last_name")
    serializer_class = ReaderSerlializer

    @action(
        detail=False,
        methods=["get"],
        name="email member discounts",
        url_path="discounts",
    )
    def send_discount_book_list_email(self, request):

        # get list of readers who are members
        list_of_readers = list(Reader.objects.filter(membership=True).values())
        list_of_discounted_books = list(Book.objects.filter(discount__gt=0).values())

        send_email_to_reader_members_about_book_discounts_task.delay(
            list_of_readers, list_of_discounted_books
        )

        return Response(
            {"message": "Emails are being sent to members about discounted books"},
            status=status.HTTP_200_OK,
        )
