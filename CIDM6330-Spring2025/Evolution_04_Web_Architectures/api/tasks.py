import random
from time import sleep
from django.core.mail import send_mail
from celery import shared_task


@shared_task()
def send_email_to_reader_members_about_book_discounts_task(
    list_of_readers, list_of_discounted_books
):

    # print (f"list of readers: {list_of_readers}")

    sleep(2)  # Simulate expensive operation(s) that freeze Django
    for reader in list_of_readers:
        email_address = reader["email"]

        message = f"Dear {reader["first_name"]}, here are some discounted books\n".join(
            [
                f"{book["title"]} - {book["discount"]}\n"
                for book in list_of_discounted_books
            ]
        )

        send_mail(
            "Discounted books",
            f"{message}\n\nThank you!",
            "info@example.com",
            [email_address],
            fail_silently=False,
        )


# simpler examples


@shared_task
def add(x, y):
    # Celery recognizes this as the `movies.tasks.add` task
    # the name is purposefully omitted here.
    return x + y


@shared_task(name="multiply_two_numbers")
def mul(x, y):
    # Celery recognizes this as the `multiple_two_numbers` task
    total = x * (y * random.randint(3, 100))
    return total


@shared_task(name="sum_list_numbers")
def xsum(numbers):
    # Celery recognizes this as the `sum_list_numbers` task
    return sum(numbers)
