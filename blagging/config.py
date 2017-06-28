import logging
import os
import sys

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = "Secret string"
    DEBUG = False
    POST_PER_PAGE = 3
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOGGING_LOCATION = 'blag.log'
    LOGGING_LEVEL = logging.DEBUG


class DevelopmentConfig(Config):
    DEBUG = True
    try:
        SQLALCHEMY_DATABASE_URI = os.environ['BLOG_DB_DEV_CONFIG_STRING']
    except KeyError:
        print("No Development DB configured")


class TestingConfig(Config):
    DEBUG = True
    WTF_CSRF_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False #Remove Debug tool bar intercept redirects or you won't be able to test them
    TESTING = True #Bubble Execptions to test framework
    try:
        SQLALCHEMY_DATABASE_URI = os.environ['BLOG_DB_TEST_CONFIG_STRING']
    except KeyError:
        print("No Test DB configured")


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    POST_PER_PAGE = 5
    try:
        SQLALCHEMY_DATABASE_URI = os.environ['BLOG_DB_CONFIG_STRING']
        SECRET_KEY = bytes(os.environ['BLOG_SECRET_STRING'].encode('utf-8'))
    except KeyError as e:
        print("No Production DB configured")


config_by_name = dict(dev=DevelopmentConfig,
                      test=TestingConfig,
                      prod=ProductionConfig)


