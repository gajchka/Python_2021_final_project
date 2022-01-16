"""
Package contains modules with views

Blueprints:
    dpt_api
    emp_api

Functions:
    to_departments()
    show_departments()
    edit_department(id_)
    delete_department(id_)
    show_employees(id_to_show=None)
    edit_employee(id_)
    delete_employee(id_)
"""
from . import view_employee
from . import view_department
