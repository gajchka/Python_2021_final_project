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
        if e.department == dpt.name:
            e.department = department
    dpt.name = department
    db.session.commit()


def delete_department(id_):

    dpt = Department.query.get(id_)
    emp = Employee.query.all()

    for e in emp:
        if e.department == dpt.name:
            db.session.delete(e)
    db.session.delete(dpt)
    db.session.commit()


def average_salary(emp, dpt):

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
