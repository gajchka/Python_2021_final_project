from department_app import db


class Department(db.Model):

    __tablename__ = 'department'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    employees = db.relationship('Employee', backref=db.backref('department', lazy=True))

    def __init__(self, name, employees=None):
        self.name = name

        if not employees:
            employees = []
        self.employees = employees

    def __repr__(self):
        return f'{self.name}'
