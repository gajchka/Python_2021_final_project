from department_app import db
from department_app.models.department import Department
from department_app.models.employee import Employee


def add_department(department):

    dpt = Department(department)
    db.session.add(dpt)
    db.session.commit()


def edit_department(id_, department):

    dpt = Department.query.get(id_)
    emp = Employee.query.all()

    for e in emp:
        if e.department == dpt.department:
            e.department = department
    dpt.department = department
    db.session.commit()


def delete_department(id_):

    dpt = Department.query.get(id_)
    emp = Employee.query.all()

    for e in emp:
        if e.department == dpt.department:
            db.session.delete(e)
    db.session.delete(dpt)
    db.session.commit()
