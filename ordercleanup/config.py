import os
from datetime import date, datetime, timedelta
from dotenv import load_dotenv

os.environ["WERKZEUG_RUN_MAIN"] = "true"
load_dotenv()

support = []
for r in  os.getenv('SUPPORT').split(','):
    support.append(str(r))

recipients = []
for r in  os.getenv('ADMINS').split(','):
    recipients.append(str(r))

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    THRESHOLD =  datetime.today() - timedelta(days=14)
    THRESHOLD = THRESHOLD.date()
    STATUS = os.getenv("STATUS")
    ROUTE_ID = os.getenv("ROUTE_ID")
    DRIVER_ID = os.getenv("DRIVER_ID")
    ARCHIVE_LEVEL = os.getenv("ARCHIVE_LEVEL") 
    IS_DEFAULT_DRIVER = os.getenv("IS_DEFAULT_DRIVER")
    PICKUP = os.getenv("PICKUP")
    DELIVERY = os.getenv("DELIVERY")
    USER_ID = os.getenv("USER_ID")
    EMPLOYEE_ID = os.getenv("EMPLOYEE_ID")
    SHIPMENT_STATUS_CODE_ID = os.getenv("SHIPMENT_STATUS_CODE_ID")
    USER_CATEGORY = os.getenv("USER_CATEGORY")
    CHANGE_DETAILS = os.getenv("CHANGE_DETAILS")
    MAIL_SERVER = 'smtp.office365.com'
    MAIL_PORT = 587
    MAIL_USERNAME = os.getenv("EMAIL")
    MAIL_DEFAULT_SENDER = os.getenv("EMAIL")
    MAIL_PASSWORD = os.getenv("MAIL_PASS")
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    RECIPIENTS = recipients
    SUPPORT = support
    SERVICE_LIST = [1,2,3,6,7,9,10,12,16,17,18,20,31,32,45,47]

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    print("DEV")
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URL")


class TestingConfig(Config):
    print("Test")
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL")


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") 
   


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}