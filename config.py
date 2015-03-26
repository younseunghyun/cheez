import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fjsldif!114F3'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:cheez@yshhome.iptime.org/wordpress'
    DEBUG = True

    @staticmethod
    def init_app(app):
        pass