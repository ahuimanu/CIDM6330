from django.db import models


# Create your models here.
class Book(models.Model):
    authors = models.ManyToManyField("Author")
    title = models.CharField(max_length=255, default="")
    publish_date = models.DateField(default=None)
    publisher = models.ForeignKey("Publisher", on_delete=models.CASCADE)
    edition = models.IntegerField(default=1, blank=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0, blank=True
    )
    discount = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.0, blank=True
    )
    isbn = models.CharField(max_length=13, default="")

    # https://stackoverflow.com/a/18108586/13355500
    def get_authors(self):
        return f"authors: ".join([f"{author.first_name} {author.last_name} " for author in self.authors.all()])    

    def __str__(self):
        return f"{self.title} by {self.get_authors()}"


class Author(models.Model):
    first_name = models.CharField(max_length=255, default="")
    middle_name = models.CharField(max_length=255, default="", blank=True)
    last_name = models.CharField(max_length=255, default="")
    email = models.EmailField(default="", blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    # https://stackoverflow.com/a/18108586/13355500
    def get_authors(self):
        return f"authors: ".join([author for author in self.authors.all()])


class Publisher(models.Model):
    name = models.CharField(max_length=255, default="")
    address = models.CharField(max_length=255, default="", blank=True)
    city = models.CharField(max_length=255, default="", blank=True)
    state = models.CharField(max_length=2, default="", blank=True)
    country = models.CharField(max_length=255, default="", blank=True)
    postcode = models.CharField(max_length=10, default="", blank=True)

    def __str__(self):
        return self.name


class Reader(models.Model):
    first_name = models.CharField(max_length=255, default="")
    middle_name = models.CharField(max_length=255, default="", blank=True)
    last_name = models.CharField(max_length=255, default="")
    email = models.EmailField(default="", blank=True)
    membership = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class FlightPlan(models.Model):
    #     id: int
    #     airline: str
    airline = models.CharField(max_length=255)
    #     flightnum: str
    flightnum = models.TextField(default="")
    #     orig: str
    origin = models.TextField(default="")
    #     dest: str
    destination = models.TextField(default="")
    #     date: int
    #     dephour: int
    #     depmin: int
    #     route: str
    #     stehour: int
    #     stemin: int
    #     altn: str
    #     pic: str
    #     picid: int
