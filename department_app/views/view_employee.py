from department_app.models.department import Department
from department_app.models.employee import Employee
from flask import render_template, Blueprint, redirect, request


emp_api = Blueprint('employee_api', __name__, template_folder='templates')
BASE_URL = 'http://127.0.0.1:5000/'


@emp_api.route('/employees', methods=('GET', 'POST'))
def show_employees():
    dpt = Department.query.all()
    emp = Employee.query.all()
    name = request.form.get('name')
    date_of_birth = request.form.get('date_of_birth')
    dpt_name = request.form.get('dpt_name')
    salary = request.form.get('salary')
    if request.method == 'POST':
        return redirect('/api/employees/add'+f'?emp_name={name}&date_of_birth={date_of_birth}'
                                             f'&dpt_name={dpt_name}&salary={salary}')
    return render_template('employees.html', departments=dpt, employees=emp)


@emp_api.route('/employees/<id_>/edit', methods=('GET', 'POST'))
def edit_employee(id_):
    dpt = Department.query.all()
    emp = Employee.query.all()
    if Employee.query.get(id_):
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
    if Employee.query.get(id_):
        return redirect('/api/employees/delete'+f'?emp_id={id_}')


