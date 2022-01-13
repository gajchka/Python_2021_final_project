"""
Module contains functions to work with Employee (CRUD operations)

Functions:
    add_employee(name, date_of_birth, salary, department)
    edit_employee(id_, name, date_of_birth, salary, department)
    delete_employee(id_)
"""
from department_app import db
from department_app.models.employee import Employee
from logging_file import logger


def add_employee(name, date_of_birth, salary, department):
    """
    Adds new employee to the db
    :param name: employee name
    :param date_of_birth: date of birth
    :param salary: salary
    :param department: department
    """
    try:
        emp = Employee(name, date_of_birth, salary, department)
        db.session.add(emp)
        db.session.commit()
        return emp
    except:
        logger.warning(f'Status: FAILED Action: DB add employee')


def edit_employee(id_, name, date_of_birth, salary, department):
    """
    Edits employee with id_
    :param id_: id of employee to edit
    :param name: employee name
    :param date_of_birth: date of birth
    :param salary: salary
    :param department: department
    """
    try:
        emp = Employee.query.get(id_)
        emp.name = name
        emp.date_of_birth = date_of_birth
        emp.salary = salary
        emp.department = department
        db.session.commit()
        return emp
    except:
        logger.warning(f'Status: FAILED Action: DB edit employee')


def delete_employee(id_):
    """
    Deletes employee with id_
    :param id_: id of employee to delete
    """
    try:
        emp = Employee.query.get(id_)
        db.session.delete(emp)
        db.session.commit()
    except:
        logger.warning(f'Status: FAILED Action: DB delete employee')
