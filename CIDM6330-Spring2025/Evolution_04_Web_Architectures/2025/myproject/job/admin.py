from django.contrib import admin

from .models import Department, Employee

# Register your models here.
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    pass

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "department", "birthdate")
    list_filter = ("department",)
    search_fields = ("first_name", "last_name")
    ordering = ("last_name", "first_name")