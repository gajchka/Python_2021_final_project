"""
Module contains functions that work with employees page

Functions:
    show_employees(id_to_show=None)
    edit_employee(id_)
    delete_employee(id_)
"""
from department_app.service.service_department import get_departments
from department_app.service.service_employee import get_employees, get_employee_id
from flask import render_template, Blueprint, redirect, request


emp_api = Blueprint('employee_api', __name__, template_folder='templates')


@emp_api.route('/employees/<id_to_show>/find', methods=['GET', 'POST'])
@emp_api.route('/employees', methods=['GET', 'POST'])
def show_employees(id_to_show=None):
    """
    On employees page adds new employee or finds employees by date of birth and renders
    employees page
    :param id_to_show: employee ids to show on page
    :return: render employees page template
    """
    dpt = get_departments()
    emp = get_employees()
    name = request.form.get('name')
    date_of_birth = request.form.get('date_of_birth')
    dpt_name = request.form.get('dpt_name')
    salary = request.form.get('salary')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    if id_to_show:
        emp.clear()
        for id_ in id_to_show.split('&'):
            for e in get_employees():
                if int(id_) == e.id:
                    emp.append(e)
    if request.method == 'POST':
        if start_date and end_date:
            return redirect('/api/employees/find' + f'?start_date={start_date}&end_date={end_date}')
        else:
            return redirect('/api/employees/add'+f'?emp_name={name}&date_of_birth={date_of_birth}'
                                             f'&dpt_name={dpt_name}&salary={salary}')
    return render_template('employees.html', departments=dpt, employees=emp)


@emp_api.route('/employees/<id_>/edit', methods=['GET', 'POST'])
def edit_employee(id_):
    """
    Edits information about employee with id_ and renders employees page template
    :param id_: id of employee to edit
    :return: render employees page template or redirects to employees page
    """
    dpt = get_departments()
    emp = get_employees()
    if get_employee_id(id_):
        if request.method == 'POST':
            name = request.form.get('edit_name')
            date_of_birth = request.form.get('edit_date_of_birth')
            department = request.form.get('edit_dpt')
            salary = request.form.get('edit_salary')
            return redirect('/api/employees/edit'+f'?emp_id={id_}&emp_name={name}&date_of_birth='
                                                  f'{date_of_birth}&dpt_name={department}&salary={salary}')
        return render_template('employees.html', id=int(id_), departments=dpt, employees=emp)
    return redirect('/employees')


@emp_api.route('/employees/<id_>/delete')
def delete_employee(id_):
    """
    Deletes employee with id_ and redirects to employees page
    :param id_: id of employee to delete
    :return: redirects to employees page
    """
    if get_employee_id(id_):
        return redirect('/api/employees/delete'+f'?emp_id={id_}')

