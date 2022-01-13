"""
This module defines is used to populate database with departments and employees,
it defines the following:

Functions:

- `populate_database`: populate database with employees and departments
"""

from datetime import date

from department_app import db, create_app
from department_app.models.department import Department
from department_app.models.employee import Employee


def populate_database():
    """
    Populate database with employees and departments

    :return: None
    """
    department_1 = Department('Department 33')
    department_2 = Department('Department 55')
    department_3 = Department('Department 77')

    employee_1 = Employee('John Watson', date(1996, 5, 12), 2000, department_1)
    employee_2 = Employee('Sherlock Holmes', date(1993, 2, 23), 2100, department_1)
    employee_3 = Employee('Mary Watson', date(1989, 11, 30), 1800, department_3)

    db.session.add(department_1)
    db.session.add(department_2)
    db.session.add(department_3)

    db.session.add(employee_1)
    db.session.add(employee_2)
    db.session.add(employee_3)

    db.session.commit()
    db.session.close()


if __name__ == '__main__':
    print('Populating database...')
    app = create_app()
    with app.app_context():
        populate_database()
    print('Successfully populated')