"""
Module contains functions that work with departments page

Functions:
    to_departments()
    show_departments()
    edit_department(id_)
    delete_department(id_)
"""
from department_app.models.department import Department
from department_app.service.service_department import average_salary
from flask import render_template, Blueprint, redirect, request


dpt_api = Blueprint('department_api', __name__, template_folder='templates')


@dpt_api.route('/')
def to_departments():
    """
    Redirects to departments page
    :return: redirect to departments page
    """
    return redirect('/departments')


@dpt_api.route('/departments', methods=('GET', 'POST'))
def show_departments():
    """
    Shows departments information or adds new department if method = 'POST' and
    renders departments page template
    :return: render departments page template
    """
    dpt = Department.query.all()
    department = request.form.get('dpt_name')
    avg_salary = average_salary()
    if request.method == 'POST':
        return redirect('/api/departments/add'+f'?dpt_name={department}')
    return render_template('departments.html', departments=dpt, avg_salary=avg_salary)


@dpt_api.route('/departments/<id_>/edit', methods=('GET', 'POST'))
def edit_department(id_):
    """
    Edits information about department with id_ and renders departments page template
    :param id_: id of department to edit
    :return: renders departments page template or redirects to departments page
    """
    dpt = Department.query.all()
    avg_salary = average_salary()
    if Department.query.get(id_):
        if request.method == 'POST':
            department = request.form.get('new_dpt')
            return redirect('/api/departments/edit'+f'?dpt_id={id_}&dpt_name={department}')
        return render_template('departments.html', id_=int(id_), departments=dpt, avg_salary=avg_salary)
    return redirect('/departments')


@dpt_api.route('/departments/<id_>/delete')
def delete_department(id_):
    """
    Deletes department with id_ and redirects to departments page
    :param id_: id of department to delete
    :return:redirects to departments page
    """
    return redirect('/api/departments/delete'+f'?dpt_id={id_}')



