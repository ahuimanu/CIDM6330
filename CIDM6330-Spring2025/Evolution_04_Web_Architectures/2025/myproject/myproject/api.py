from datetime import date

from django.shortcuts import get_object_or_404

from ninja import NinjaAPI
from ninja import Schema
from ninja import UploadedFile, File

from job.models import Employee

# Thsi is an input schema for the Employee model
class EmployeeIn(Schema):
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: date = None

class EmployeeOut(Schema):
    id: int
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: date = None

api = NinjaAPI()

@api.get("/hello")
def hello(request):
    return {"message": "Hello, World!"}

@api.get("/add")
def add(request, a: int, b: int):
    return {"result": a + b}

@api.post("/employees")
def create_employee(request, employee: EmployeeIn, cv: UploadedFile = File(...)):
    worker_info = employee.dict()
    worker = Employee(**worker_info)
    employee = Employee.objects.create(worker)    
    employee.cv.save(cv.name, cv)

    return employee

@api.get("/employees/{employee_id}", response=EmployeeOut)
def get_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    return employee

@api.get("/employees", response=list[EmployeeOut])
def list_empoloyees(request):
    employees = Employee.objects.all()
    return employees

@api.put("/employees/{employee_id}")
def update_employee(request, employee_id: int, payload: EmployeeIn):
    employee = get_object_or_404(Employee, id=employee_id)
    # employee.first_name = employee.first_name
    # employee.last_name = employee.last_name
    # employee.department_id = employee.department_id
    # employee.birthdate = employee.birthdate
    for attr, value in payload.dict().items():
        setattr(employee, attr, value)
    employee.save()
    return {"success": True, "employee": employee}

@api.delete("/employees/{employee_id}")
def delete_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    employee.delete()
    return {"success": True, "employee": employee}