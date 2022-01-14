import unittest
from department_app import create_app, db
from populate import populate_database
from config import TestConfig
from department_app.models.department import Department

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

    # test / page receiving get request
    def test_to_departments(self):
        rv = self.client.get('/')
        self.assertEqual(rv.status, '302 FOUND')

    # test /departments page receiving get request
    def test_show_departments_get(self):
        rv = self.client.get('/departments')
        self.assertEqual(rv.status, '200 OK')
        for dpt in Department.query.all():
            self.assertIn(dpt.name, rv.get_data(as_text=True))
        for i in ['2050.0', 'No employees yet', '1800.0']:
            self.assertIn(i, rv.get_data(as_text=True))

    # test /departments page receiving post request
    def test_show_departments_post(self):
        rv = self.client.post('/departments', data=dict(dpt_name='DPT'), follow_redirects=True)
        self.assertEqual(rv.status, '200 OK')
        self.assertIn('DPT', rv.get_data(as_text=True))

    # test /departments/<id>/edit receiving get request
    def test_edit_department_get(self):
        rv = self.client.get('/departments/1/edit', data=dict(new_dpt='NEW DPT'), follow_redirects=True)
        self.assertEqual(rv.status, '200 OK')
        self.assertNotIn('NEW DPT', rv.get_data(as_text=True))
        self.assertIn('Submit', rv.get_data(as_text=True))

    # test /departments/<id>/edit receiving post request and invalid id
    def test_edit_department_no_id(self):
        rv = self.client.post('/departments/5/edit', data=dict(new_dpt='NEW DPT'), follow_redirects=True)
        self.assertEqual(rv.status, '200 OK')
        self.assertNotIn('NEW DPT', rv.get_data(as_text=True))

    # test /departments/<id>/edit receiving post request
    def test_edit_department_post(self):
        rv = self.client.post('/departments/1/edit', data=dict(new_dpt='NEW DPT'), follow_redirects=True)
        self.assertEqual(rv.status, '200 OK')
        self.assertIn('NEW DPT', rv.get_data(as_text=True))
        self.assertNotIn('Department 33', rv.get_data(as_text=True))

    # test /departments/<id>/delete receiving get request
    def test_delete_department(self):
        rv = self.client.get('/departments/2/delete', follow_redirects=True)
        self.assertEqual(rv.status, '200 OK')
        self.assertNotIn('Department 55', rv.get_data(as_text=True))

    # test /departments/<id>/edit receiving get request and invalid id
    def test_delete_department_no_id(self):
        rv = self.client.get('/departments/5/delete', follow_redirects=True)
        self.assertEqual(rv.status, '200 OK')
        for dpt in Department.query.all():
            self.assertIn(dpt.name, rv.get_data(as_text=True))


if __name__ == '__main__':
    unittest.main()
