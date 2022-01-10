from department_app.models.department import Department
from department_app.models.employee import Employee
from department_app.service.service_department import average_salary
from flask import render_template, Blueprint, redirect, request


dpt_api = Blueprint('department_api', __name__, template_folder='templates')
BASE_URL = 'http://127.0.0.1:5000/'


@dpt_api.route('/')
def to_departments():
    #dpt = Department.query.all()
    #emp = Employee.query.all()
    #avg_salary = average_salary(emp, dpt)
    #return avg_salary
    return redirect('/departments')


@dpt_api.route('/departments', methods=('GET', 'POST'))
def show_departments():
    dpt = Department.query.all()
    emp = Employee.query.all()
    department = request.form.get('dpt_name')
    avg_salary = average_salary(emp, dpt)
    if request.method == 'POST':
        return redirect('/api/departments/add'+f'?dpt_name={department}')
    return render_template('departments.html', departments=dpt, avg_salary=avg_salary)


@dpt_api.route('/departments/<id_>/edit', methods=('GET', 'POST'))
def edit_department(id_):
    dpt = Department.query.all()
    emp = Employee.query.all()
    avg_salary = average_salary(emp, dpt)
    if Department.query.get(id_):
        if request.method == 'POST':
            department = request.form.get('new_dpt')
            return redirect('/api/departments/edit'+f'?dpt_id={id_}&dpt_name={department}')
        return render_template('departments.html', id_=int(id_), departments=dpt, avg_salary=avg_salary)
    return redirect('/departments')


@dpt_api.route('/departments/<id_>/delete')
def delete_department(id_):
    if Department.query.get(id_):
        return redirect('/api/departments/delete'+f'?dpt_id={id_}')



