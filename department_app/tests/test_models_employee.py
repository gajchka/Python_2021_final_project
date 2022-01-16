import unittest
import datetime
from department_app import create_app, db
from populate import populate_database
from department_app.models.employee import Employee
from config import TestConfig

app = create_app(TestConfig)


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        populate_database()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # test Employee class
    def test_employee(self):
        emp = Employee.query.get(1)
        self.assertEqual(emp.name, 'John Watson')
        self.assertEqual(emp.date_of_birth, datetime.date(1996, 5, 12))
        self.assertEqual(emp.salary, 2000)
        self.assertEqual(emp.department.name, 'Department 33')
        self.assertEqual(str(emp), '1, John Watson, 1996-05-12, Department 33, 2000')



if __name__ == '__main__':
    unittest.main()
