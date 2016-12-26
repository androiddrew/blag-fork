import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = "Secret string"
    DEBUG = False
    POST_PER_PAGE = 3


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'devblagging.db')


class TestingConfig(Config):
    DEBUG = True
    WTF_CSRF_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False #Remove Debug tool bar intercept redirects or you won't be able to test them
    TESTING = True #Bubble Execptions to test framework
    try:
        SQLALCHEMY_DATABASE_URI = os.environ['BLOG_DB_TEST_CONFIG_STRING']
    except KeyError:
        pass


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    POST_PER_PAGE = 10
    try:
        SQLALCHEMY_DATABASE_URI = os.environ['BLOG_DB_CONFIG_STRING']
        SECRET_KEY = bytes(os.environ['BLOG_SECRET_STRING'].encode('utf-8'))
    except KeyError:
        pass


config_by_name = dict(dev=DevelopmentConfig,
                      test=TestingConfig,
                      prod=ProductionConfig)


