"""
Module contains app instance and runs application
"""
from department_app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)