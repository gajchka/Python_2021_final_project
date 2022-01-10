from flask_restful import Resource, reqparse
from flask import redirect
from department_app.service.service_employee import add_employee, edit_employee, delete_employee
from department_app.models.employee import Employee
from department_app.models.department import Department
from datetime import datetime

add_arg = reqparse.RequestParser()
add_arg.add_argument('emp_name', type=str, help='Name of the new employee', required=True)
add_arg.add_argument('date_of_birth', type=str, help='Date of birth', required=True)
add_arg.add_argument('dpt_name', type=str, help='Department name', required=True)
add_arg.add_argument('salary', type=int, help='Salary', required=True)


edit_arg = reqparse.RequestParser()
edit_arg.add_argument('emp_id', type=int, help='Id of the employee to edit', required=True)
edit_arg.add_argument('emp_name', type=str, help='New name of the employee', required=True)
edit_arg.add_argument('date_of_birth', type=str, help=' New date of birth', required=True)
edit_arg.add_argument('dpt_name', type=str, help='New department name', required=True)
edit_arg.add_argument('salary', type=int, help='New salary', required=True)


del_arg = reqparse.RequestParser()
del_arg.add_argument('emp_id', type=int, help='Id of the employee to delete', required=True)

find_arg = reqparse.RequestParser()
find_arg.add_argument('start_date', type=str, help='Start date of the requested period', required=True)
find_arg.add_argument('end_date', type=str, help='End date of the requested period', required=True)


class EmployeesAPIget(Resource):

    def get(self):
        emp_qry = Employee.query.all()
        employees = dict()
        for ind, emp in enumerate(emp_qry):
            employees[ind] = {'id': emp.id, 'name': emp.name, 'date_of_birth': emp.date_of_birth,
                              'salary': emp.salary, 'department': emp.department}
        return employees


class EmployeesAPIadd(Resource):

    def get(self):
        arg = add_arg.parse_args()
        emp_name = arg['emp_name']
        date_of_birth = arg['date_of_birth']
        salary = int(arg['salary'])
        dpt_name = arg['dpt_name']
        if Department.query.filter_by(name=dpt_name).first() and emp_name and emp_name.strip() \
                and salary > 0:
            date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
            dpt = Department.query.filter_by(name=dpt_name).first()
            add_employee(emp_name, date_of_birth, salary, dpt)
            return redirect('/employees')


class EmployeesAPIedit(Resource):

    def get(self):
        arg = edit_arg.parse_args()
        emp_id = arg['emp_id']
        emp_name = arg['emp_name']
        date_of_birth = arg['date_of_birth']
        salary = int(arg['salary'])
        dpt_name = arg['dpt_name']
        if Employee.query.get(emp_id) and Department.query.filter_by(name=dpt_name).first() \
                and emp_name and emp_name.strip() and salary > 0:
            date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
            dpt = Department.query.filter_by(name=dpt_name).first()
            edit_employee(emp_id, emp_name, date_of_birth, salary, dpt)
            return redirect('/employees')


class EmployeesAPIdelete(Resource):

    def get(self):
        arg = del_arg.parse_args()
        emp_id = arg['emp_id']
        if Employee.query.get(emp_id):
            delete_employee(emp_id)
            return redirect('/employees')


class EmployeesAPIfind(Resource):

    def get(self):
        arg = find_arg.parse_args()
        start_date = arg['start_date']
        end_date = arg['end_date']

        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        if start_date > end_date:
            raise ValueError
        emp_qry = Employee.query.filter(Employee.date_of_birth.between(start_date, end_date)).all()
        employees = dict()
        id_to_send = ''
        for ind, emp in enumerate(emp_qry):
            id_to_send = id_to_send + str(emp.id) + '&'
            employees[ind] = {'id': emp.id, 'name': emp.name, 'date_of_birth': str(emp.date_of_birth),
                              'salary': emp.salary, 'department': emp.department}
        if emp_qry:
            return redirect(f'/employees/{id_to_send[0:-1]}/find')

        return employees
