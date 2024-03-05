from django.contrib import admin
from .models import Bookmark, Snippet

# Register your models here.
admin.site.register(Bookmark)
admin.site.register(Snippet)
