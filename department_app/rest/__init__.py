from . import rest_employee
from . import rest_department
from department_app import api


def init_api():

    api.add_resource(rest_department.DepartmentsAPIadd, '/api/departments/add')
    api.add_resource(rest_department.DepartmentsAPIget, '/api/departments/get')
    api.add_resource(rest_department.DepartmentsAPIedit, '/api/departments/edit')
    api.add_resource(rest_department.DepartmentAPIdelete, '/api/departments/delete')

    api.add_resource(rest_employee.EmployeesAPIadd, '/api/employees/add')
    api.add_resource(rest_employee.EmployeesAPIget, '/api/employees/get')
    api.add_resource(rest_employee.EmployeesAPIedit, '/api/employees/edit')
    api.add_resource(rest_employee.EmployeesAPIdelete, '/api/employees/delete')
    api.add_resource(rest_employee.EmployeesAPIfind, '/api/employees/find')
