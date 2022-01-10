from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.app_context().push()
    db.init_app(app)
    #db.create_all()

    from department_app.views.view_department import dpt_api
    from department_app.views.view_employee import emp_api
    app.register_blueprint(dpt_api)
    app.register_blueprint(emp_api)

    from department_app.rest import init_api, api
    init_api()
    api.init_app(app)
    return app
