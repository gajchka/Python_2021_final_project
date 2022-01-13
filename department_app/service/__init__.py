"""
Package contains modules with functions to work with DB (CRUD operations)

Functions:
    get_departments()
    get_department_id(id_)
    get_department_name(dpt_name)
    add_department(department)
    edit_department(id_, department)
    delete_department(id_)
    average_salary()
    get_employees()
    get_employee_id(id_)
    add_employee(name, date_of_birth, salary, department)
    edit_employee(id_, name, date_of_birth, salary, department)
    delete_employee(id_)
"""
from . import service_department
from . import service_employee
