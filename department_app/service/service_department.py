"""
Module contains functions to work with Department (CRUD operations)

Functions:
    get_departments()
    get_department_id(id_)
    get_department_name(dpt_name)
    add_department(department)
    edit_department(id_, department)
    delete_department(id_)
    average_salary()
"""
from department_app import db
from department_app.models.department import Department
from department_app.models.employee import Employee
from logging_file import logger


def get_departments():
    """
    Gets all departments from db
    :return: list of all departments
    """
    return Department.query.all()


def get_department_id(id_):
    """
    Gets department with id_ from db
    :return: department with id_
    """
    try:
        return Department.query.get(id_)
    except:
        logger.warning(f'Status: FAILED Action: DB get department by id')


def get_department_name(dpt_name):
    """
    Gets department by name from db
    :return: department with name dpt_name
    """
    dpt = Department.query.filter_by(name=dpt_name).first()
    if not dpt:
        logger.warning(f'Status: FAILED Action: DB get department by name')
    else:
        return dpt


def add_department(department):
    """
    Adds new department to the db
    :param department: department name
    """
    try:
        dpt = Department(department)
        db.session.add(dpt)
        db.session.commit()
        return dpt
    except:
        logger.warning(f'Status: FAILED Action: DB add department')


def edit_department(id_, department):
    """
    Edits department with id_
    :param id_: department id
    :param department: new department name
    """
    try:
        dpt = Department.query.get(id_)
        emp = Employee.query.all()
        for e in emp:
            if e.department == dpt.name:
                e.department = department
        dpt.name = department
        db.session.commit()
        return dpt
    except:
        logger.warning(f'Status: FAILED Action: DB edit department')


def delete_department(id_):
    """
    Deletes department with id_ and employees in it
    :param id_: department id
    """
    try:
        dpt = Department.query.get(id_)
        emp = Employee.query.all()
        for e in emp:
            if e.department.name == dpt.name:
                db.session.delete(e)
        db.session.delete(dpt)
        db.session.commit()
    except:
        logger.warning(f'Status: FAILED Action: DB delete department')


def average_salary():
    """
    Returns dict with departments and their average salary
    :return: dict with departments and their average salary
    """
    dpt = Department.query.all()
    emp = Employee.query.all()
    total_salary = dict()
    avg_salary = dict()
    for d in dpt:
        total_salary[d.id] = []
    for e in emp:
        for d in dpt:
            if e.department.name == d.name:
                total_salary[d.id].append(e.salary)
    for dep, sal in total_salary.items():
        if len(sal) != 0:
            avg_salary[dep] = sum(sal)/len(sal)
        else:
            avg_salary[dep] = 'No employees yet'
    return avg_salary
