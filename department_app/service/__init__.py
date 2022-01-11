"""
Package contains modules with functions to work with DB (CRUD operations)

Functions:
    add_department(department)
    edit_department(id_, department)
    delete_department(id_)
    average_salary(emp, dpt)
    add_employee(name, date_of_birth, salary, department)
    edit_employee(id_, name, date_of_birth, salary, department)
    delete_employee(id_)
"""
from . import service_department
from . import service_employee
