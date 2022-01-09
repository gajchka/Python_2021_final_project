from flask_restful import Resource, reqparse
from department_app.service.service_department import add_department, edit_department, delete_department, average_salary
from department_app.models.department import Department


add_arg = reqparse.RequestParser()
add_arg.add_argument('dpt_name', type=str, help='Name of the new department', required=True)

edit_arg = reqparse.RequestParser()
edit_arg.add_argument('dpt_id', type=int, help='Id of the department to edit', required=True)
edit_arg.add_argument('dpt_name', type=str, help='New department name', required=True)

del_arg = reqparse.RequestParser()
del_arg.add_argument('dpt_id', type=int, help='Id of the department to delete', required=True)


class DepartmentsAPIget(Resource):

    def get(self):
        dpt_qry = Department.query.all()
        avg_salary = average_salary()
        dpt_dict = dict()
        for ind, dpt in enumerate(dpt_qry):
            dpt_dict[f'{ind}'] = {'id': dpt.id, 'department': dpt.name, 'avg_salary': avg_salary}
        return dpt_dict


class DepartmentsAPIadd(Resource):

    def get(self):
        arg = add_arg.parse_args()
        dpt_name = arg['dpt_name']
        if dpt_name and dpt_name.strip() and not Department.query.filter_by(name=dpt_name).first():
            add_department(dpt_name)
            return {'message': 'ADD_SUCCESS'}


class DepartmentsAPIedit(Resource):

    def get(self):
        arg = edit_arg.parse_args()
        dpt_name = arg['dpt_name']
        dpt_id = arg['dpt_id']
        if dpt_name and dpt_name.strip() and Department.query.get(dpt_id):
            edit_department(dpt_id, dpt_name)
            return {'message': 'EDIT_SUCCESS'}


class DepartmentAPIdelete(Resource):

    def get(self):
        arg = del_arg.parse_args()
        dpt_id = arg['dpt_id']
        if Department.query.get(dpt_id):
            delete_department(dpt_id)
            return {'message': 'DELETE_SUCCESS'}

