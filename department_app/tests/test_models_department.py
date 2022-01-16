import unittest
from department_app import create_app, db
from populate import populate_database
from department_app.models.department import Department
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

    # test Department class
    def test_department(self):
        dpt = Department.query.get(1)
        self.assertEqual(dpt.name, 'Department 33')
        self.assertEqual(str(dpt), 'Department 33')
        self.assertEqual(str(dpt.employees), '[1, John Watson, 1996-05-12, Department 33, 2000, '
                                             '2, Sherlock Holmes, 1993-02-23, Department 33, 2100]')

        dpt2 = Department.query.get(2)
        self.assertEqual(dpt2.employees, [])


if __name__ == '__main__':
    unittest.main()
