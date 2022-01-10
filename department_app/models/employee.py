from department_app import db


class Employee(db.Model):

    __tablename__ = 'employee'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    salary = db.Column(db.Integer, nullable=False)

    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))

    def __init__(self, name, date_of_birth, salary, department):
        self.name = name
        self.date_of_birth = date_of_birth
        self.salary = salary
        self.department = department

    def __repr__(self):
        return f'Employee {self.name}, date of birth: {self.date_of_birth}, salary:{self.salary}'
