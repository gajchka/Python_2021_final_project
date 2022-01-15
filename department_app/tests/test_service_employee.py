import unittest
from config import TestConfig
from department_app import create_app, db
from populate import populate_database
from datetime import date
from department_app.models.employee import Employee
from department_app.models.department import Department
from department_app.service.service_employee import add_employee, edit_employee, delete_employee, get_employees, get_employee_id

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

    # test get_employees function
    def test_get_employees(self):
        emp = get_employees()
        self.assertEqual(len(emp), 3)
        self.assertEqual(emp, Employee.query.all())

    # test get_employee_id function on valid data
    def test_get_employee_id(self):
        emp = get_employee_id(1)
        self.assertEqual(emp.name, 'John Watson')
        self.assertEqual(emp.date_of_birth, date(1996, 5, 12))
        self.assertEqual(emp.salary, 2000)
        self.assertEqual(emp.department, Department.query.get(1))

    # test get_employee_id function on valid data
    def test_get_employee_id_err(self):
        with self.assertLogs('my_logger', 'INFO') as cm:
            emp = get_employee_id(5)
            self.assertEqual(emp, None)
            self.assertEqual(cm.output, ['INFO:my_logger:Employee with id: 5 not found'])

    # test add_employee function on valid data
    def test_employee_add(self):
        emp = add_employee('Anna', date(1996, 5, 12), 1000, Department.query.get(1))
        self.assertEqual(emp.name, 'Anna')
        self.assertEqual(emp.date_of_birth, date(1996, 5, 12))
        self.assertEqual(emp.salary, 1000)
        self.assertEqual(emp.department.id, 1)
        self.assertEqual(emp, Employee.query.get(4))
        self.assertEqual(len(Employee.query.all()), 4)

    # test add_employee function on invalid data
    def test_employee_add_err(self):
        with self.assertLogs('my_logger', 'INFO') as cm:
            add_employee('Anna', date(1996, 5, 12), 1000, 1)
            add_employee('Anna', '12-11-1998', 1000, Department.query.get(1))
            self.assertEqual(cm.output, ['WARNING:my_logger:Status: FAILED Action: DB add employee']*2)

    # test edit_employee function on valid data
    def test_employee_edit(self):
        emp = edit_employee(1, 'Ann', date(1997, 5, 12), 1100, Department.query.get(1))
        self.assertEqual(emp.name, 'Ann')
        self.assertEqual(emp.date_of_birth, date(1997, 5, 12))
        self.assertEqual(emp.salary, 1100)
        self.assertEqual(emp.department.id, 1)
        self.assertEqual(emp, Employee.query.get(1))
        self.assertEqual(len(Employee.query.all()), 3)

    # test edit_employee function on invalid data
    def test_employee_edit_err(self):
        with self.assertLogs('my_logger', 'INFO') as cm:
            edit_employee(4, 'Ann', date(1997, 5, 12), 1100, Department.query.get(1))
            edit_employee(1, 'Anna', date(1996, 5, 12), 1000, 1)
            edit_employee(1, 'Anna', '12-11-1998', 1000, Department.query.get(1))
            self.assertEqual(cm.output, ['WARNING:my_logger:Status: FAILED Action: DB edit employee']*3)

    # test delete_employee function
    def test_employee_delete(self):
        delete_employee(3)
        self.assertEqual(len(Employee.query.all()), 2)
        self.assertEqual(Employee.query.get(3), None)
        with self.assertLogs('my_logger', 'INFO') as cm:
            delete_employee(4)
            self.assertEqual(cm.output, ['WARNING:my_logger:Status: FAILED Action: DB delete employee'])


if __name__ == '__main__':
    unittest.main()
