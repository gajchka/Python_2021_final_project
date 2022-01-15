

class Config:
    """
    Main configuration
    """
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    """
    Configuration for testing
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tests/test_db.db'
    WTF_CSRF_ENABLED = False