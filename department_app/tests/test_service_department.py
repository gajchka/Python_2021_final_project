import unittest
from department_app import create_app, db
from populate import populate_database
from config import TestConfig
from department_app.models.department import Department
from department_app.service.service_department import add_department, edit_department, \
    delete_department, average_salary, get_departments, get_department_name, get_department_id

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

    # test get_departments function
    def test_get_departments(self):
        dpt = get_departments()
        self.assertEqual(len(dpt), 3)
        self.assertEqual(dpt, Department.query.all())

    # test get_department_id function
    def test_get_department_id(self):
        dpt = get_department_id(1)
        self.assertEqual(dpt.name, 'Department 33')
        with self.assertLogs('my_logger', 'INFO') as cm:
            dpt1 = get_department_id(5)
            self.assertEqual(dpt1, None)
            self.assertEqual(cm.output, ['INFO:my_logger:Department with id: 5 not found'])

    # test get_department_name function
    def test_get_department_name(self):
        dpt = get_department_name('Department 33')
        self.assertEqual(dpt.id, 1)
        with self.assertLogs('my_logger', 'INFO') as cm:
            dpt1 = get_department_name('Dpt')
            self.assertEqual(dpt1, None)
            self.assertEqual(cm.output, ['INFO:my_logger:Department with name: Dpt not found'])


    # test add_department function on valid data
    def test_department_add(self):
        dpt = add_department('Department 111')
        self.assertEqual(dpt.name, 'Department 111')
        self.assertEqual(dpt, Department.query.get(4))
        self.assertEqual(len(Department.query.all()), 4)

    # test add_department function on invalid data
    def test_department_add_err(self):
        with self.assertLogs('my_logger', 'INFO') as cm:
            add_department([111])
            self.assertEqual(cm.output, ['WARNING:my_logger:Status: FAILED Action: DB add department'])

    # test edit_department function on valid data
    def test_department_edit(self):
        dpt = edit_department(1, 'Department 111')
        self.assertEqual(dpt.name, 'Department 111')
        self.assertEqual(dpt, Department.query.get(1))
        self.assertEqual(len(Department.query.all()), 3)

    # test edit_department function on invalid data
    def test_department_edit_err(self):
        with self.assertLogs('my_logger', 'INFO') as cm:
            edit_department(1, ['Department 111'])
            edit_department(4, 'Department 111')
            self.assertEqual(cm.output, ['WARNING:my_logger:Status: FAILED Action: DB edit department']*2)

    # test delete_department function
    def test_department_delete(self):
        delete_department(1)
        self.assertEqual(len(Department.query.all()), 2)
        self.assertEqual(Department.query.get(1), None)
        with self.assertLogs('my_logger', 'INFO') as cm:
            delete_department(4)
            self.assertEqual(cm.output, ['WARNING:my_logger:Status: FAILED Action: DB delete department'])

    def test_average_salary(self):
        avg_salary = average_salary()
        self.assertEqual(avg_salary, {1: 2050.0, 2: 'No employees yet', 3: 1800.0})


if __name__ == '__main__':
    unittest.main()
