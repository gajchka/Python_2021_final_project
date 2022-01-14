import unittest
from department_app import create_app, db
from populate import populate_database
from config import TestConfig
from department_app.models.employee import Employee

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

    # test /employees page receiving get request
    def test_show_employees_get(self):
        rv = self.client.get('/employees', follow_redirects=True)
        self.assertEqual(rv.status, '200 OK')
        info = ['John Watson', '1996-05-12', '2000', 'Department 33',
                'Sherlock Holmes', '1993-02-23', '2100',
                'Mary Watson', '1989-11-30', '1800', 'Department 77']
        for i in info:
            self.assertIn(i, rv.get_data(as_text=True))

    # test /employees page receiving post request
    def test_employees_post(self):
        rv = self.client.post('/employees', data=dict(name='Elizabeth', date_of_birth='1986-12-12',
                                                      dpt_name='Department 33', salary='1250'),
                              follow_redirects=True)
        self.assertEqual(rv.status, '200 OK')
        for i in ['Elizabeth', '1986-12-12', 'Department 33', '1250']:
            self.assertIn(i, rv.get_data(as_text=True))

    # test /employees/<id_to_show>/find receiving get request
    def test_employees_find_get(self):
        rv = self.client.get('/employees/1&2/find', follow_redirects=True)
        self.assertEqual(rv.status, '200 OK')
        info = ['John Watson', '1996-05-12', '2000', 'Department 33',
                'Sherlock Holmes', '1993-02-23', '2100', 'Department 33']
        for i in info:
            self.assertIn(i, rv.get_data(as_text=True))
        for j in ['Mary Watson', '1989-11-30', '1800']:
            self.assertNotIn(j, rv.get_data(as_text=True))

    # test /employees/<id_to_show>/find receiving post request
    def test_employees_find_post(self):
        rv = self.client.post('/employees', data=dict(start_date='1992-12-12', end_date='1997-12-11'),
                              follow_redirects=True)
        self.assertEqual(rv.status, '200 OK')
        info = ['John Watson', '1996-05-12', '2000', 'Department 33',
                'Sherlock Holmes', '1993-02-23', '2100', 'Department 33']
        for i in info:
            self.assertIn(i, rv.get_data(as_text=True))
        for j in ['Mary Watson', '1989-11-30', '1800']:
            self.assertNotIn(j, rv.get_data(as_text=True))

    # test /employees/<id>/delete receiving get request
    def test_delete_employee(self):
        rv = self.client.get('/employees/2/delete', follow_redirects=True)
        self.assertEqual(rv.status, '200 OK')
        self.assertNotIn('Sherlock Holmes', rv.get_data(as_text=True))

    # test /employees/<id>/delete receiving get request and invalid id
    def test_delete_employee_no_id(self):
        rv = self.client.get('/employees/5/delete', follow_redirects=True)
        self.assertEqual(rv.status, '200 OK')
        for emp in Employee.query.all():
            self.assertIn(emp.name, rv.get_data(as_text=True))


if __name__ == '__main__':
    unittest.main()
