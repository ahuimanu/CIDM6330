from django.contrib import admin
from .models import Author, Book, Publisher, Reader


# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "get_authors",
        "publisher",
        "publish_date",
        "edition",
        "isbn",
    ]

    # https://stackoverflow.com/a/18108586/13355500
    def get_authors(self, obj):
        # https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
        return f"authors: ".join(
            [f"{author.first_name} {author.last_name}" for author in obj.authors.all()]
        )


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["first_name", "middle_name", "last_name", "email"]


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ["name", "address", "city", "state", "country", "postcode"]


@admin.register(Reader)
class ReaderAdmin(admin.ModelAdmin):
    list_display = ["first_name", "middle_name", "last_name", "email", "membership"]
