"""
Module contains classes that work with REST Api for Employees

Classes:
    EmployeesAPIadd(Resource)
    EmployeesAPIedit(Resource)
    EmployeesAPIdelete(Resource)
    EmployeesAPIfind(Resource)
"""
from datetime import datetime
from flask_restful import Resource, reqparse
from flask import redirect
from logging_file import logger
from department_app.service.service_employee import add_employee, edit_employee, \
    delete_employee, get_employees, get_employee_id
from department_app.service.service_department import get_department_name
from department_app.models.employee import Employee


add_arg = reqparse.RequestParser()
add_arg.add_argument('emp_name', type=str, help='Name of the new employee', required=True)
add_arg.add_argument('date_of_birth', type=str, help='Date of birth', required=True)
add_arg.add_argument('dpt_name', type=str, help='Department name', required=True)
add_arg.add_argument('salary', type=str, help='Salary', required=True)

edit_arg = reqparse.RequestParser()
edit_arg.add_argument('emp_id', type=int, help='Id of the employee to edit', required=True)
edit_arg.add_argument('emp_name', type=str, help='New name of the employee', required=True)
edit_arg.add_argument('date_of_birth', type=str, help=' New date of birth', required=True)
edit_arg.add_argument('dpt_name', type=str, help='New department name', required=True)
edit_arg.add_argument('salary', type=str, help='New salary', required=True)

del_arg = reqparse.RequestParser()
del_arg.add_argument('emp_id', type=int, help='Id of the employee to delete', required=True)

find_arg = reqparse.RequestParser()
find_arg.add_argument('start_date', type=str, help='Start date of requested period', required=True)
find_arg.add_argument('end_date', type=str, help='End date of requested period', required=True)


def check_data_unique(name, dob, dpt, salary):
    """
    Checks if an employee with the given data already exists
    :param name: employee name
    :param dob: date of birth
    :param dpt: department
    :param salary: salary
    :return: bool value
    """
    emp = get_employees()
    for e in emp:
        if e.name == name and e.date_of_birth == dob and e.department.name == dpt and \
                e.salary == salary:
            return False
    return True


class EmployeesAPIadd(Resource):
    """
    Class inherits from class Resource and is responsible for adding
    new employee to the table

    Methods:
        get(self)
    """
    def get(self):
        """
        In case of valid input data adds new employee and redirects to employees page.
        In case of invalid data redirects to employees page.
        :return: redirects to employees page
        """
        arg = add_arg.parse_args()
        emp_name = arg['emp_name'].strip()
        date_of_birth = arg['date_of_birth']
        salary = arg['salary']
        dpt_name = arg['dpt_name']
        try:
            salary = int(salary)
            date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
            dpt = get_department_name(dpt_name)
            if dpt and emp_name and salary > 0 and date_of_birth \
                    and check_data_unique(emp_name, date_of_birth, dpt_name, salary):
                add_employee(emp_name, date_of_birth, salary, dpt)
                logger.info(f'Status: SUCCESS Action: adding employee name: {emp_name}, date of birth: '
                            f'{date_of_birth}, department: {dpt_name}, salary: {salary}')
                return redirect('/employees')
            raise ValueError
        except:
            logger.info(f'Status: FAILED Action: adding employee name: {emp_name}, date of birth: '
                        f'{date_of_birth}, department: {dpt_name}, salary: {salary}')
            return redirect('/employees')


class EmployeesAPIedit(Resource):
    """
    Class inherits from class Resource and is responsible for editing
    information about employees

    Methods:
        get(self)
    """
    def get(self):
        """
        In case of valid input data changes info about employee with given id and
        redirects to employees page. In case of invalid data redirects to employees page.
        :return: redirects to employees page
        """
        arg = edit_arg.parse_args()
        emp_id = arg['emp_id']
        emp_name = arg['emp_name'].strip()
        date_of_birth = arg['date_of_birth']
        salary = arg['salary']
        dpt_name = arg['dpt_name']
        try:
            salary = int(salary)
            date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
            if get_employee_id(emp_id) and get_department_name(dpt_name) \
                    and emp_name and salary > 0 and date_of_birth \
                    and check_data_unique(emp_name, date_of_birth, dpt_name, salary):
                dpt = get_department_name(dpt_name)
                edit_employee(emp_id, emp_name, date_of_birth, salary, dpt)
                logger.info(f'Status: SUCCESS Action: editing employee id: {emp_id}, name: '
                            f'{emp_name}, date of birth: {date_of_birth}, department: '
                            f'{dpt_name}, salary: {salary}')
                return redirect('/employees')
            raise ValueError
        except:
            logger.info(f'Status: FAILED Action: editing employee id: {emp_id}, name: {emp_name}, '
                        f'date of birth: {date_of_birth}, department: {dpt_name}, salary: {salary}')
            return redirect('/employees')


class EmployeesAPIdelete(Resource):
    """
    Class inherits from class Resource and is responsible for deleting
    employees from the table

    Methods:
        get(self)
    """
    def get(self):
        """
        Deletes employee by id and redirects to employees page
        :return: redirects to employees page
        """
        arg = del_arg.parse_args()
        emp_id = arg['emp_id']
        if get_employee_id(emp_id):
            delete_employee(emp_id)
            logger.info(f'Status: SUCCESS Action: deleting employee id: {emp_id}')
            return redirect('/employees')
        logger.info(f'Status: FAILED Action: deleting employee id: {emp_id}')
        return redirect('/employees')


class EmployeesAPIfind(Resource):
    """
    Class inherits from class Resource and is responsible for finding
    employees whose date of birth is between chosen dates

    Methods:
        get(self)
    """
    def get(self):
        """
        In case of invalid input data redirects to employees page.
        In case of valid input data finds ids of employees with fitting date of birth
        and redirects to employees page with ids formatted as a string
        :return: redirects to employees page with|without ids of employees
        """
        arg = find_arg.parse_args()
        start_date = arg['start_date']
        end_date = arg['end_date']

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            if start_date > end_date:
                raise ValueError
            emp_qry = Employee.query.filter(Employee.date_of_birth.between(start_date, end_date)).all()
            id_to_send = ''
            for emp in emp_qry:
                id_to_send = id_to_send + str(emp.id) + '&'
            logger.info(f'Status: SUCCESS Action: finding employee by date of birth start date: '
                        f'{start_date}, end date: {end_date}. Result ids: {id_to_send[0:-1]}')
            if emp_qry:
                return redirect(f'/employees/{id_to_send[0:-1]}/find')
            return redirect('/employees/0/find')
        except:
            logger.info(f'Status: FAILED Action: finding employee by date of birth start date: '
                        f'{start_date}, end date: {end_date}')
            return redirect('/employees')
