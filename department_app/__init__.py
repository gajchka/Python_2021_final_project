"""
Initializes web application and web service, contains following packages and
modules:
    migrations: contains migration files used to manage database schema
    models: contains modules with Python classes describing database models
    rest: contains modules with RESTful service implementation
    service: contains modules with functions to work with database
    static: contains web application static files (images)
    templates: contains web application html templates
    views: contains modules with views
    tests: contains modules with unit tests
"""
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app(conf=Config):
    """
    Creates app and merges it with database, blueprints and rest
    :return: flask application instance
    """
    app = Flask(__name__)
    app.config.from_object(conf)
    db.init_app(app)
    migrate.init_app(app, db)

    from department_app.views.view_department import dpt_api
    from department_app.views.view_employee import emp_api
    app.register_blueprint(dpt_api)
    app.register_blueprint(emp_api)

    from department_app.rest import init_api, api
    init_api()
    api.init_app(app)
    return app
