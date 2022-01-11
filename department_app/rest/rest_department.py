"""
Module contains classes that work with REST Api for Employees

Classes:
    EmployeesAPIget(Resource)
    EmployeesAPIadd(Resource)
    EmployeesAPIedit(Resource)
    EmployeesAPIdelete(Resource)
    EmployeesAPIfind(Resource)
"""
from flask_restful import Resource, reqparse
from flask import redirect
from department_app.service.service_department import add_department, edit_department, delete_department, average_salary
from department_app.models.department import Department
from logging_file import logger


add_arg = reqparse.RequestParser()
add_arg.add_argument('dpt_name', type=str, help='Name of the new department', required=True)

edit_arg = reqparse.RequestParser()
edit_arg.add_argument('dpt_id', type=int, help='Id of the department to edit', required=True)
edit_arg.add_argument('dpt_name', type=str, help='New department name', required=True)

del_arg = reqparse.RequestParser()
del_arg.add_argument('dpt_id', type=int, help='Id of the department to delete', required=True)


class DepartmentsAPIget(Resource):
    """
    Class inherits from class Resource and is responsible for getting
    information about departments

    Methods:
        get(self)
    """
    def get(self):
        """
        Gets information about all departments in the table
        :return: dict of departments and information about them
        """
        dpt_qry = Department.query.all()
        avg_salary = average_salary()
        dpt_dict = dict()
        for ind, dpt in enumerate(dpt_qry):
            dpt_dict[f'{ind}'] = {'id': dpt.id, 'department': dpt.name, 'avg_salary': avg_salary}
        return dpt_dict


class DepartmentsAPIadd(Resource):
    """
    Class inherits from class Resource and is responsible for adding
    new departments to the table

    Methods:
        get(self)
    """
    def get(self):
        """
        In case of valid input data adds new department and redirects to departments page.
        In case of invalid data redirects to departments page.
        :return:redirects to departments page
        """
        arg = add_arg.parse_args()
        dpt_name = arg['dpt_name'].strip()
        if dpt_name and not Department.query.filter_by(name=dpt_name).first():
            add_department(dpt_name)
            logger.info(f'Status: SUCCESS Action: adding {dpt_name}')
            return redirect('/departments')
        logger.info(f'Status: FAILED Action: adding {dpt_name}')
        return redirect('/departments')


class DepartmentsAPIedit(Resource):
    """
    Class inherits from class Resource and is responsible for editing
    information about departments

    Methods:
        get(self)
    """
    def get(self):
        """
        In case of valid input data changes name of department with given id and redirects to departments page.
        In case of invalid data redirects to departments page.
        :return: redirects to departments page
        """
        arg = edit_arg.parse_args()
        dpt_name = arg['dpt_name'].strip()
        dpt_id = arg['dpt_id']
        if dpt_name and Department.query.get(dpt_id) and \
                dpt_name not in list(map(lambda x: x.name, Department.query.all())):
            edit_department(dpt_id, dpt_name)
            logger.info(f'Status: SUCCESS Action: editing department id: {dpt_id}, new name: {dpt_name}')
            return redirect('/departments')
        logger.info(f'Status: FAILED Action: editing department id: {dpt_id}, new name: {dpt_name}')
        return redirect('/departments')


class DepartmentAPIdelete(Resource):
    """
    Class inherits from class Resource and is responsible for deleting
    departments from the table

    Methods:
        get(self)
    """
    def get(self):
        """
        Deletes department by id and redirects to departments page
        :return: redirects to departments page
        """
        arg = del_arg.parse_args()
        dpt_id = arg['dpt_id']
        if Department.query.get(dpt_id):
            delete_department(dpt_id)
            logger.info(f'Status: SUCCESS Action: deleting department id: {dpt_id}')
            return redirect('/departments')
        logger.info(f'Status: FAILED Action: deleting department id: {dpt_id}')
        return redirect('/departments')

