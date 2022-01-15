import unittest
from department_app import create_app, db
from populate import populate_database
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

    # test method of class DepartmentsAPIadd with valid data
    def test_department_api_add(self):
        with self.assertLogs('my_logger', level='INFO') as cm:
            rv = self.client.get('/api/departments/add?dpt_name=Department')
            self.assertEqual(rv.status, '302 FOUND')
            self.assertEqual(cm.output, ['INFO:my_logger:Department with name: Department not found',
                                         'INFO:my_logger:Status: SUCCESS Action: adding Department'])

    # test method of class DepartmentsAPIadd with invalid data
    def test_department_api_add_err(self):
        with self.assertLogs('my_logger', level='INFO') as cm:
            self.client.get('/api/departments/add?dpt_name=')
            self.client.get('/api/departments/add?dpt_name=   ')
            self.client.get('/api/departments/add?dpt_name=Department 33')
            self.assertEqual(cm.output, ['INFO:my_logger:Status: FAILED Action: adding ',
                                         'INFO:my_logger:Status: FAILED Action: adding ',
                                         'INFO:my_logger:Status: FAILED Action: adding Department 33'])

    # test method of class DepartmentsAPIedit with valid data
    def test_department_api_edit(self):
        with self.assertLogs('my_logger', level='INFO') as cm:
            rv = self.client.get('/api/departments/edit?dpt_id=1&dpt_name=Department')
            self.assertEqual(rv.status, '302 FOUND')
            self.assertEqual(cm.output, ['INFO:my_logger:Status: SUCCESS Action: editing department id: 1,'
                                         ' new name: Department'])

    # test method of class DepartmentsAPIedit with invalid data
    def test_department_api_edit_err(self):
        with self.assertLogs('my_logger', level='INFO') as cm:
            self.client.get('/api/departments/edit?dpt_id=1&dpt_name=')
            self.client.get('/api/departments/edit?dpt_id=1&dpt_name=   ')
            self.client.get('/api/departments/edit?dpt_id=1&dpt_name=Department 33')
            self.client.get('/api/departments/edit?dpt_id=5&dpt_name=Department 48')
            self.assertEqual(cm.output, ['INFO:my_logger:Status: FAILED Action: editing department id: 1, new name: ',
                                         'INFO:my_logger:Status: FAILED Action: editing department id: 1, new name: ',
                                         'INFO:my_logger:Status: FAILED Action: editing department id: 1, new name: '
                                         'Department 33', 'INFO:my_logger:Department with id: 5 not found',
                                         'INFO:my_logger:Status: FAILED Action: editing department id: 5, new name: '
                                         'Department 48'])

    # test method of class DepartmentsAPIdelete with valid data
    def test_department_api_delete(self):
        with self.assertLogs('my_logger', level='INFO') as cm:
            rv = self.client.get('/api/departments/delete?dpt_id=1')
            self.assertEqual(rv.status, '302 FOUND')
            self.assertEqual(cm.output, ['INFO:my_logger:Status: SUCCESS Action: deleting department id: 1'])

    # test method of class DepartmentsAPIdelete with invalid data
    def test_department_api_delete_err(self):
        with self.assertLogs('my_logger', level='INFO') as cm:
            self.client.get('/api/departments/delete?dpt_id=5')
            self.assertEqual(cm.output, ['INFO:my_logger:Department with id: 5 not found',
                                         'INFO:my_logger:Status: FAILED Action: deleting department id: 5'])


if __name__ == '__main__':
    unittest.main()
