import unittest
from department_app import create_app, db
from populate import populate_database
from config import TestConfig
from datetime import date
from department_app.rest.rest_employee import check_data_unique

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

    # test method of class EmployeesAPIadd with valid data
    def test_employee_api_add(self):
        with self.assertLogs('my_logger', level='INFO') as cm:
            rv = self.client.get('/api/employees/add?emp_name=Anna&date_of_birth=1993-12-13'
                                 '&dpt_name=Department 33&salary=500')
            self.assertEqual(rv.status, '302 FOUND')
            self.assertEqual(cm.output, ['INFO:my_logger:Status: SUCCESS Action: adding employee name: Anna, '
                                         'date of birth: 1993-12-13, department: Department 33, salary: 500'])

    # test method of class EmployeesAPIadd with invalid name
    def test_employee_api_add_err1(self):
        with self.assertLogs('my_logger', level='INFO') as cm:
            rv = self.client.get('/api/employees/add?emp_name=&date_of_birth=1993-12-13'
                                 '&dpt_name=Department 33&salary=500')
            self.assertEqual(rv.status, '302 FOUND')
            self.assertEqual(cm.output, ['INFO:my_logger:Status: FAILED Action: adding employee name: , '
                                         'date of birth: 1993-12-13, department: Department 33, salary: 500'])

    # test method of class EmployeesAPIadd with invalid department
    def test_employee_api_add_err2(self):
        with self.assertLogs('my_logger', level='INFO') as cm:
            rv = self.client.get('/api/employees/add?emp_name=Anna&date_of_birth=1993-12-13'
                                 '&dpt_name=Department 48&salary=500')
            self.assertEqual(rv.status, '302 FOUND')
            self.assertEqual(cm.output, ['INFO:my_logger:Department with name: Department 48 not found',
                                         'INFO:my_logger:Status: FAILED Action: adding employee name: Anna, '
                                         'date of birth: 1993-12-13, department: Department 48, salary: 500'])

    # test method of class EmployeesAPIadd with invalid salary (not integer)
    def test_employee_api_add_err3(self):
        with self.assertLogs('my_logger', level='INFO') as cm:
            rv = self.client.get('/api/employees/add?emp_name=Anna&date_of_birth=1993-12-13'
                                 '&dpt_name=Department 33&salary=abc')
            self.assertEqual(rv.status, '302 FOUND')
            self.assertEqual(cm.output, ['INFO:my_logger:Status: FAILED Action: adding employee name: Anna, '
                                         'date of birth: 1993-12-13, department: Department 33, salary: abc'])

    # test method of class EmployeesAPIadd with invalid salary (salary<0)
    def test_employee_api_add_err4(self):
        with self.assertLogs('my_logger', level='INFO') as cm:
            rv = self.client.get('/api/employees/add?emp_name=Anna&date_of_birth=1993-12-13'
                                 '&dpt_name=Department 33&salary=-1000')
            self.assertEqual(rv.status, '302 FOUND')
            self.assertEqual(cm.output, ['INFO:my_logger:Status: FAILED Action: adding employee name: Anna, '
                                         'date of birth: 1993-12-13, department: Department 33, salary: -1000'])

    # test method of class EmployeesAPIadd with invalid date of birth
    def test_employee_api_add_err5(self):
        with self.assertLogs('my_logger', level='INFO') as cm:
            rv = self.client.get('/api/employees/add?emp_name=Anna&date_of_birth='
                                 '&dpt_name=Department 33&salary=1000')
            self.assertEqual(rv.status, '302 FOUND')
            self.assertEqual(cm.output, ['INFO:my_logger:Status: FAILED Action: adding employee name: Anna, '
                                         'date of birth: , department: Department 33, salary: 1000'])

    # test method of class EmployeesAPIadd with invalid date of birth (invalid format)
    def test_employee_api_add_err6(self):
        with self.assertLogs('my_logger', level='INFO') as cm:
            rv = self.client.get('/api/employees/add?emp_name=Anna&date_of_birth=12.12.1996'
                                 '&dpt_name=Department 33&salary=1000')
            self.assertEqual(rv.status, '302 FOUND')
            self.assertEqual(cm.output, ['INFO:my_logger:Status: FAILED Action: adding employee name: Anna, '
                                         'date of birth: 12.12.1996, department: Department 33, salary: 1000'])

    # test method of class EmployeesAPIadd with invalid data (employee already exists)
    def test_employee_api_add_err7(self):
        with self.assertLogs('my_logger', level='INFO') as cm:
            rv = self.client.get('/api/employees/add?emp_name=John Watson&date_of_birth=1996-05-12'
                                 '&dpt_name=Department 33&salary=2000')
            self.assertEqual(rv.status, '302 FOUND')
            self.assertEqual(cm.output, ['INFO:my_logger:Status: FAILED Action: adding employee name: John Watson, '
                                         'date of birth: 1996-05-12, department: Department 33, salary: 2000'])

    # test method of class EmployeesAPIedit with valid data
    def test_employee_api_edit(self):
        with self.assertLogs('my_logger', level='INFO') as cm:
            rv = self.client.get('/api/employees/edit?emp_id=1&emp_name=Anna&date_of_birth=1993-12-13'
                                 '&dpt_name=Department 33&salary=500')
            self.assertEqual(rv.status, '302 FOUND')
            self.assertEqual(cm.output, ['INFO:my_logger:Status: SUCCESS Action: editing employee id: 1, name: Anna, '
                                         'date of birth: 1993-12-13, department: Department 33, salary: 500'])

    # test method of class EmployeesAPIedit with invalid name
    def test_employee_api_edit_err1(self):
        with self.assertLogs('my_logger', level='INFO') as cm:
            rv = self.client.get('/api/employees/edit?emp_id=1&emp_name=&date_of_birth=1993-12-13'
                                 '&dpt_name=Department 33&salary=500')
            self.assertEqual(rv.status, '302 FOUND')
            self.assertEqual(cm.output, ['INFO:my_logger:Status: FAILED Action: editing employee id: 1, name: , '
                                         'date of birth: 1993-12-13, department: Department 33, salary: 500'])

    # test method of class EmployeesAPIedit with invalid department
    def test_employee_api_edit_err2(self):
        with self.assertLogs('my_logger', level='INFO') as cm:
            rv = self.client.get('/api/employees/edit?emp_id=1&emp_name=Anna&date_of_birth=1993-12-13'
                                 '&dpt_name=Department 48&salary=500')
            self.assertEqual(rv.status, '302 FOUND')
            self.assertEqual(cm.output, ['INFO:my_logger:Department with name: Department 48 not found',
                                         'INFO:my_logger:Status: FAILED Action: editing employee id: 1, name: Anna, '
                                         'date of birth: 1993-12-13, department: Department 48, salary: 500'])

    # test method of class EmployeesAPIedit with invalid salary (not integer)
    def test_employee_api_edit_err3(self):
        with self.assertLogs('my_logger', level='INFO') as cm:
            rv = self.client.get('/api/employees/edit?emp_id=1&emp_name=Anna&date_of_birth=1993-12-13'
                                 '&dpt_name=Department 33&salary=abc')
            self.assertEqual(rv.status, '302 FOUND')
            self.assertEqual(cm.output, ['INFO:my_logger:Status: FAILED Action: editing employee id: 1, name: Anna, '
                                         'date of birth: 1993-12-13, department: Department 33, salary: abc'])

    # test method of class EmployeesAPIedit with invalid salary (salary<0)
    def test_employee_api_edit_err4(self):
        with self.assertLogs('my_logger', level='INFO') as cm:
            rv = self.client.get('/api/employees/edit?emp_id=1&emp_name=Anna&date_of_birth=1993-12-13'
                                 '&dpt_name=Department 33&salary=-1000')
            self.assertEqual(rv.status, '302 FOUND')
            self.assertEqual(cm.output, ['INFO:my_logger:Status: FAILED Action: editing employee id: 1, name: Anna, '
                                         'date of birth: 1993-12-13, department: Department 33, salary: -1000'])

    # test method of class EmployeesAPIedit with invalid date of birth
    def test_employee_api_edit_err5(self):
        with self.assertLogs('my_logger', level='INFO') as cm:
            rv = self.client.get('/api/employees/edit?emp_id=1&emp_name=Anna&date_of_birth='
                                 '&dpt_name=Department 33&salary=1000')
            self.assertEqual(rv.status, '302 FOUND')
            self.assertEqual(cm.output, ['INFO:my_logger:Status: FAILED Action: editing employee id: 1, name: Anna, '
                                         'date of birth: , department: Department 33, salary: 1000'])

    # test method of class EmployeesAPIedit with invalid date of birth (invalid format)
    def test_employee_api_edit_err6(self):
        with self.assertLogs('my_logger', level='INFO') as cm:
            rv = self.client.get('/api/employees/edit?emp_id=1&emp_name=Anna&date_of_birth=12.12.1996'
                                 '&dpt_name=Department 33&salary=1000')
            self.assertEqual(rv.status, '302 FOUND')
            self.assertEqual(cm.output, ['INFO:my_logger:Status: FAILED Action: editing employee id: 1, name: Anna, '
                                         'date of birth: 12.12.1996, department: Department 33, salary: 1000'])

    # test method of class EmployeesAPIedit with invalid data (employee already exists)
    def test_employee_api_edit_err7(self):
        with self.assertLogs('my_logger', level='INFO') as cm:
            rv = self.client.get('/api/employees/edit?emp_id=2&emp_name=John Watson&date_of_birth=1996-05-12'
                                 '&dpt_name=Department 33&salary=2000')
            self.assertEqual(rv.status, '302 FOUND')
            self.assertEqual(cm.output, ['INFO:my_logger:Status: FAILED Action: editing employee id: 2, name: John '
                                         'Watson, date of birth: 1996-05-12, department: Department 33, salary: 2000'])

    # test method of class EmployeesAPIedit with invalid id
    def test_employee_api_edit_err8(self):
        with self.assertLogs('my_logger', level='INFO') as cm:
            rv = self.client.get('/api/employees/edit?emp_id=5&emp_name=Anna&date_of_birth=1993-12-13'
                                 '&dpt_name=Department 33&salary=500')
            self.assertEqual(rv.status, '302 FOUND')
            self.assertEqual(cm.output, ['INFO:my_logger:Employee with id: 5 not found', 'INFO:my_logger:Status: FAILED'
                                         ' Action: editing employee id: 5, name: Anna, '
                                         'date of birth: 1993-12-13, department: Department 33, salary: 500'])

    # test method of class EmployeesAPIdelete with valid data
    def test_employee_api_delete(self):
        with self.assertLogs('my_logger', level='INFO') as cm:
            rv = self.client.get('/api/employees/delete?emp_id=1')
            self.assertEqual(rv.status, '302 FOUND')
            self.assertEqual(cm.output, ['INFO:my_logger:Status: SUCCESS Action: deleting employee id: 1'])

    # test method of class EmployeesAPIdelete with invalid id
    def test_employee_api_delete_err(self):
        with self.assertLogs('my_logger', level='INFO') as cm:
            rv = self.client.get('/api/employees/delete?emp_id=5')
            self.assertEqual(rv.status, '302 FOUND')
            self.assertEqual(cm.output, ['INFO:my_logger:Employee with id: 5 not found',
                                         'INFO:my_logger:Status: FAILED Action: deleting employee id: 5'])

    # test method of class EmployeesAPIfind with valid data
    def test_employee_api_find(self):
        with self.assertLogs('my_logger', level='INFO') as cm:
            rv = self.client.get('/api/employees/find?start_date=1992-12-12&end_date=1997-10-10')
            self.assertEqual(rv.status, '302 FOUND')
            self.assertEqual(cm.output, ['INFO:my_logger:Status: SUCCESS Action: finding employee by date of birth '
                                         'start date: 1992-12-12, end date: 1997-10-10. Result ids: 1&2'])
        with self.assertLogs('my_logger', level='INFO') as cm2:
            rv2 = self.client.get('/api/employees/find?start_date=1996-05-12&end_date=1996-05-12')
            self.assertEqual(rv2.status, '302 FOUND')
            self.assertEqual(cm2.output, ['INFO:my_logger:Status: SUCCESS Action: finding employee by date of birth '
                                          'start date: 1996-05-12, end date: 1996-05-12. Result ids: 1'])
        with self.assertLogs('my_logger', level='INFO') as cm3:
            rv3 = self.client.get('/api/employees/find?start_date=1997-05-12&end_date=1998-05-12')
            self.assertEqual(rv3.status, '302 FOUND')
            self.assertEqual(cm3.output, ['INFO:my_logger:Status: SUCCESS Action: finding employee by date of birth '
                                          'start date: 1997-05-12, end date: 1998-05-12. Result ids: '])
            self.assertEqual(rv3.location, 'http://localhost/employees/0/find')

    # test method of class EmployeesAPIfind with invalid date format
    def test_employee_api_find_err1(self):
        with self.assertLogs('my_logger', level='INFO') as cm:
            rv = self.client.get('/api/employees/find?start_date=1992.12.12&end_date=1997-10-10')
            self.assertEqual(rv.status, '302 FOUND')
            self.assertEqual(cm.output, ['INFO:my_logger:Status: FAILED Action: finding employee by date of birth '
                                         'start date: 1992.12.12, end date: 1997-10-10'])

    # test method of class EmployeesAPIfind with invalid data (start date < end date)
    def test_employee_api_find_err2(self):
        with self.assertLogs('my_logger', level='INFO') as cm:
            rv = self.client.get('/api/employees/find?start_date=1998-12-12&end_date=1997-10-10')
            self.assertEqual(rv.status, '302 FOUND')
            self.assertEqual(cm.output, ['INFO:my_logger:Status: FAILED Action: finding employee by date of birth '
                                         'start date: 1998-12-12, end date: 1997-10-10'])

    # test check_data_unique function
    def test_check_unique(self):
        self.assertTrue(check_data_unique('random', date(1996, 5, 12), 'Department 33', 1000))
        self.assertFalse(check_data_unique('John Watson', date(1996, 5, 12), 'Department 33', 2000))
        self.assertTrue(check_data_unique('John Watson', date(1996, 5, 11), 'Department 33', 2000))


if __name__ == '__main__':
    unittest.main()
