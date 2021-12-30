from department_app import db
from department_app.models.employee import Employee


def add_employee(name, date_of_birth, salary, department):

    emp = Employee(name, date_of_birth, salary, department)
    db.session.add(emp)
    db.session.commit()


def edit_department(id_, name, date_of_birth, salary, department):

    emp = Employee.query.get(id_)
    emp.name = name
    emp.date_of_birth = date_of_birth
    emp.salary = salary
    emp.department = department
    db.session.commit()


def delete_department(id_):

    emp = Employee.query.get(id_)
    db.session.delete(emp)
    db.session.commit()
