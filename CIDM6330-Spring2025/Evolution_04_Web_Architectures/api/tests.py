from datetime import datetime
from django.test import TestCase
from .models import Book

# author = models.CharField(max_length=255, default="")
# title = models.CharField(max_length=255, default="")
# year = models.DateField(default=None)
# publisher = models.CharField(max_length=255, default="")
# isbn = models.CharField(max_length=13)


# Create your tests here.
class BookTestCase(TestCase):
    def setUp(self):
        # arrange
        Book.objects.create(
            author="Me",
            title="Myself",
            year="2024-11-01",
            publisher="And I",
            isbn="1234567890123",
        )

    def test_book_date_is_not_future(self):
        # act
        book = Book.objects.get(author="Me")
        # assert
        self.assertLessEqual(book.year.year, datetime.now().year)
