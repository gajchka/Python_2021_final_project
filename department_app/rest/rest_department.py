"""
Module contains classes that work with REST Api for Departments

Classes:
    DepartmentsAPIadd(Resource)
    DepartmentsAPIedit(Resource)
    DepartmentAPIdelete(Resource)
"""
from flask_restful import Resource, reqparse
from flask import redirect
from department_app.service.service_department import add_department, edit_department, \
    delete_department, get_department_id, get_departments, get_department_name
from logging_file import logger


add_arg = reqparse.RequestParser()
add_arg.add_argument('dpt_name', type=str, help='Name of the new department', required=True)

edit_arg = reqparse.RequestParser()
edit_arg.add_argument('dpt_id', type=int, help='Id of the department to edit', required=True)
edit_arg.add_argument('dpt_name', type=str, help='New department name', required=True)

del_arg = reqparse.RequestParser()
del_arg.add_argument('dpt_id', type=int, help='Id of the department to delete', required=True)


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
        if dpt_name and not get_department_name(dpt_name):
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
        In case of valid input data changes name of department with given id and redirects to
        departments page. In case of invalid data redirects to departments page.
        :return: redirects to departments page
        """
        arg = edit_arg.parse_args()
        dpt_name = arg['dpt_name'].strip()
        dpt_id = arg['dpt_id']
        if dpt_name and get_department_id(dpt_id) and \
                dpt_name not in list(map(lambda x: x.name, get_departments())):
            edit_department(dpt_id, dpt_name)
            logger.info(f'Status: SUCCESS Action: editing department id: {dpt_id}, new name: '
                        f'{dpt_name}')
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
        if get_department_id(dpt_id):
            delete_department(dpt_id)
            logger.info(f'Status: SUCCESS Action: deleting department id: {dpt_id}')
            return redirect('/departments')
        logger.info(f'Status: FAILED Action: deleting department id: {dpt_id}')
        return redirect('/departments')
