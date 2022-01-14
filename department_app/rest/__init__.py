"""
Package contains modules with classes that work with REST Api

Classes:
    EmployeesAPIadd(Resource)
    EmployeesAPIedit(Resource)
    EmployeesAPIdelete(Resource)
    EmployeesAPIfind(Resource)
    DepartmentsAPIadd(Resource)
    DepartmentsAPIedit(Resource)
    DepartmentAPIdelete(Resource)
"""
from flask_restful import Api
from . import rest_employee
from . import rest_department

api = Api()


def init_api():
    """
    Adds resources to api
    """
    api.add_resource(rest_department.DepartmentsAPIadd, '/api/departments/add')
    api.add_resource(rest_department.DepartmentsAPIedit, '/api/departments/edit')
    api.add_resource(rest_department.DepartmentAPIdelete, '/api/departments/delete')

    api.add_resource(rest_employee.EmployeesAPIadd, '/api/employees/add')
    api.add_resource(rest_employee.EmployeesAPIedit, '/api/employees/edit')
    api.add_resource(rest_employee.EmployeesAPIdelete, '/api/employees/delete')
    api.add_resource(rest_employee.EmployeesAPIfind, '/api/employees/find')
